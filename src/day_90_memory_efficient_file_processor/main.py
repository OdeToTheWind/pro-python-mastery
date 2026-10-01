"""Day 90 – Capstone: Memory-efficient Large File Processor.

Scenario: a *DNA-sequencing lab* receives FASTQ files far larger than RAM.
Reads are streamed in fixed-size binary chunks, re-assembled into lines and
4-line records, quality-filtered, counted, and sorted with an *external*
merge sort – and ``tracemalloc`` proves the peak memory stays flat while the
file grows.

Deliverables (syllabus):
* Chunking (fixed-size binary reads; lines that straddle chunk borders)
* Streaming generators (records → filter → statistics, one pass)
* Bounded-memory algorithms (external merge sort with ``heapq.merge``)
* ``mmap`` scanning and measuring peak memory with ``tracemalloc``
"""

from __future__ import annotations

import heapq
import itertools
import mmap
import random
import tempfile
import tracemalloc
from collections import Counter
from collections.abc import Callable, Iterable, Iterator
from contextlib import ExitStack
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any

DELIVERABLES: dict[str, str] = {
    "fixed-size chunk reader": "read_chunks",
    "lines across chunk borders": "lines_from_chunks",
    "streaming record parser": "parse_fastq",
    "quality filter pipeline": "filter_reads",
    "single-pass statistics": "stream_stats",
    "external merge sort": "external_sort",
    "mmap pattern search": "mmap_count",
    "peak memory measurement": "peak_memory",
}


@dataclass(frozen=True, slots=True)
class Read:
    name: str
    sequence: str
    quality: str

    @property
    def mean_quality(self) -> float:
        """Phred+33: each character encodes a quality score."""
        return sum(ord(c) - 33 for c in self.quality) / len(self.quality) if self.quality else 0.0

    def to_fastq(self) -> str:
        return f"@{self.name}\n{self.sequence}\n+\n{self.quality}\n"


def read_chunks(path: Path, size: int = 1 << 16) -> Iterator[bytes]:
    with path.open("rb") as handle:
        while chunk := handle.read(size):
            yield chunk


def lines_from_chunks(chunks: Iterable[bytes]) -> Iterator[str]:
    """Keep the unfinished tail of each chunk and glue it to the next one."""
    tail = b""
    for chunk in chunks:
        *complete, tail = (tail + chunk).split(b"\n")
        for line in complete:
            yield line.decode("ascii").rstrip("\r")
    if tail:
        yield tail.decode("ascii").rstrip("\r")


def parse_fastq(lines: Iterable[str]) -> Iterator[Read]:
    it = (line.rstrip("\r\n") for line in lines)  # accepts open files as well as stripped lines
    for number, header in enumerate(it):
        if not header:
            continue
        block = list(itertools.islice(it, 3))
        if not header.startswith("@") or len(block) < 3 or not block[1].startswith("+"):
            raise ValueError(f"malformed record #{number + 1}: {header[:30]!r}")
        sequence, _, quality = block
        if len(sequence) != len(quality):
            raise ValueError(f"{header[1:]}: sequence/quality length mismatch")
        yield Read(header[1:], sequence, quality)


def filter_reads(reads: Iterable[Read], *, min_quality: float = 30.0, min_length: int = 20,
                 max_n: float = 0.1) -> Iterator[Read]:
    for read in reads:
        if (len(read.sequence) >= min_length and read.mean_quality >= min_quality
                and read.sequence.count("N") <= max_n * len(read.sequence)):
            yield read


def stream_stats(reads: Iterable[Read], k: int = 3, top: int = 3) -> dict[str, Any]:
    """Counts, GC content and frequent k-mers – memory grows with 4**k, never with file size."""
    n = bases = gc = 0
    kmers: Counter[str] = Counter()
    for read in reads:
        n += 1
        bases += len(read.sequence)
        gc += read.sequence.count("G") + read.sequence.count("C")
        kmers.update(read.sequence[i:i + k] for i in range(len(read.sequence) - k + 1))
    return {"reads": n, "bases": bases, "gc_percent": round(100 * gc / bases, 1) if bases else 0.0,
            "top_kmers": kmers.most_common(top)}


def external_sort(reads: Iterable[Read], out: Path, *, key: Callable[[Read], str] = lambda r: r.sequence,
                  max_in_memory: int = 1000, work_dir: Path | None = None) -> int:
    """Sort runs of ``max_in_memory`` reads to temp files, then k-way merge them lazily."""
    runs: list[Path] = []
    with tempfile.TemporaryDirectory(dir=work_dir) as tmp:
        source = iter(reads)
        for index in itertools.count():
            batch = list(itertools.islice(source, max_in_memory))  # only this run is ever in memory
            if not batch:
                break
            run = Path(tmp) / f"run-{index:05d}.fastq"
            run.write_text("".join(r.to_fastq() for r in sorted(batch, key=key)), encoding="ascii")
            runs.append(run)
        with ExitStack() as stack, out.open("w", encoding="ascii") as dest:
            streams = [parse_fastq(stack.enter_context(r.open(encoding="ascii"))) for r in runs]
            written = 0
            for read in heapq.merge(*(s for s in streams), key=key):
                dest.write(read.to_fastq())
                written += 1
    return written


def mmap_count(path: Path, pattern: bytes) -> int:
    """The OS pages the file in on demand – searching never copies it into Python memory."""
    if path.stat().st_size == 0:
        return 0
    with path.open("rb") as handle, mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        count, pos = 0, mm.find(pattern)
        while pos != -1:
            count += 1
            pos = mm.find(pattern, pos + 1)
        return count


def peak_memory(func: Callable[[], object]) -> tuple[object, int]:
    tracemalloc.start()
    try:
        result = func()
        _current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return result, peak


def generate_fastq(path: Path, n: int, length: int = 60, seed: int = 90) -> Path:
    rng = random.Random(seed)
    with path.open("w", encoding="ascii") as handle:
        for i in range(n):
            seq = "".join(rng.choices("ACGT", k=length))
            if i % 10 == 0:
                seq = "N" * (length // 5) + seq[length // 5:]
            qual = "".join(chr(33 + rng.randint(20, 40) - (15 if i % 7 == 0 else 0)) for _ in range(length))
            handle.write(Read(f"read{i}", seq, qual).to_fastq())
    return path


def process(path: Path, chunk_size: int = 1 << 16) -> dict[str, Any]:
    return stream_stats(filter_reads(parse_fastq(lines_from_chunks(read_chunks(path, chunk_size)))))


def main() -> None:
    print("Day 90 – Streaming FASTQ processor\n")
    with tempfile.TemporaryDirectory() as tmp:
        for n in (2_000, 20_000):
            path = generate_fastq(Path(tmp) / f"reads-{n}.fastq", n)
            stats, peak = peak_memory(partial(process, path))
            print(f"{path.stat().st_size / 1e6:5.1f} MB file → peak {peak / 1e3:6.0f} kB  {stats}")
        sorted_path = Path(tmp) / "sorted.fastq"
        reads = parse_fastq(lines_from_chunks(read_chunks(Path(tmp) / "reads-2000.fastq")))
        print("externally sorted reads:", external_sort(reads, sorted_path, max_in_memory=300))
        print("GATTACA occurrences:", mmap_count(Path(tmp) / "reads-20000.fastq", b"GATTACA"))


if __name__ == "__main__":
    main()
