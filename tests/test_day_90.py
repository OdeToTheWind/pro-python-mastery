"""Tests for Day 90 – Memory-efficient Large File Processor."""

import pytest

from src.day_90_memory_efficient_file_processor.main import (
    Read,
    external_sort,
    filter_reads,
    generate_fastq,
    lines_from_chunks,
    main,
    mmap_count,
    parse_fastq,
    peak_memory,
    process,
    read_chunks,
    stream_stats,
)


def test_chunks_and_line_reassembly(tmp_path):
    path = tmp_path / "x.txt"
    path.write_bytes(b"alpha\r\nbeta\ngamma")
    assert [len(c) for c in read_chunks(path, 4)] == [4, 4, 4, 4, 1]
    assert list(lines_from_chunks(read_chunks(path, 3))) == ["alpha", "beta", "gamma"]
    assert list(lines_from_chunks([b"a\n", b""])) == ["a"]


@pytest.mark.parametrize("chunk", [1, 7, 64, 1 << 16])
def test_result_does_not_depend_on_chunk_size(tmp_path, chunk):
    path = generate_fastq(tmp_path / "r.fastq", 50)
    assert process(path, chunk) == process(path)


def test_parse_fastq_and_errors():
    good = ["@r1", "ACGT", "+", "IIII", "", "@r2", "AC", "+r2", "!!"]
    reads = list(parse_fastq(good))
    assert reads == [Read("r1", "ACGT", "IIII"), Read("r2", "AC", "!!")]
    assert reads[0].mean_quality == 40.0 and reads[1].mean_quality == 0.0 and Read("e", "", "").mean_quality == 0
    with pytest.raises(ValueError, match="length mismatch"):
        list(parse_fastq(["@r", "ACG", "+", "II"]))
    with pytest.raises(ValueError, match="malformed record"):
        list(parse_fastq(["r1", "A", "+", "I"]))
    with pytest.raises(ValueError, match="malformed"):
        list(parse_fastq(["@r1", "A"]))


def test_filter_rules():
    hi = "I" * 25
    reads = [Read("ok", "A" * 25, hi), Read("short", "A" * 5, "I" * 5),
             Read("lowq", "A" * 25, "+" * 25), Read("nnn", "N" * 5 + "A" * 20, hi)]
    assert [r.name for r in filter_reads(reads)] == ["ok"]
    assert [r.name for r in filter_reads(reads, max_n=0.5)] == ["ok", "nnn"]


def test_stream_stats():
    stats = stream_stats([Read("a", "GGCA", "IIII"), Read("b", "GGCC", "IIII")], k=2, top=1)
    assert stats == {"reads": 2, "bases": 8, "gc_percent": 87.5, "top_kmers": [("GG", 2)]}
    assert stream_stats([])["gc_percent"] == 0.0


def test_external_sort_matches_in_memory_sort(tmp_path):
    path = generate_fastq(tmp_path / "r.fastq", 257)
    reads = list(parse_fastq(path.read_text().splitlines()))
    out = tmp_path / "sorted.fastq"
    assert external_sort(iter(reads), out, max_in_memory=40, work_dir=tmp_path) == 257
    assert [r.sequence for r in parse_fastq(out.read_text().splitlines())] == sorted(r.sequence for r in reads)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["r.fastq", "sorted.fastq"]  # runs cleaned up


def test_mmap_count(tmp_path):
    path = tmp_path / "s.txt"
    path.write_bytes(b"AAAA GATTACA xx GATTACA")
    assert mmap_count(path, b"GATTACA") == 2 and mmap_count(path, b"AA") == 3
    (tmp_path / "empty").write_bytes(b"")
    assert mmap_count(tmp_path / "empty", b"A") == 0


def test_peak_memory_stays_flat_as_file_grows(tmp_path):
    small = generate_fastq(tmp_path / "s.fastq", 500)
    big = generate_fastq(tmp_path / "b.fastq", 5_000)
    _, small_peak = peak_memory(lambda: process(small, 4096))
    _, big_peak = peak_memory(lambda: process(big, 4096))
    _, eager_peak = peak_memory(lambda: big.read_text().splitlines())
    assert big.stat().st_size > 9 * small.stat().st_size
    assert big_peak < 2 * small_peak and big_peak < eager_peak / 4


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "externally sorted reads: 2000" in out and "GATTACA occurrences:" in out
