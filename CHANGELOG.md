# Changelog

All notable changes to CorruptChain are documented here. The format follows
Keep a Changelog, and the project uses semantic versioning.

## [Unreleased]

### Changed

- Unknown verdict wording is under review for the next patch.

## [1.0.4] - 2026-07-21

### Fixed

- The inferred edge finder no longer matches a value that appears only in a
  step's own output.

## [1.0.3] - 2025-11-18

### Fixed

- A trace with no answer step reports unknown with a reason line instead of an
  empty verdict block.

## [1.0.2] - 2024-10-15

### Added

- The empty degraded class and its rule: status empty, or ok with no output,
  or result_count zero.

## [1.0.1] - 2023-08-29

### Fixed

- Inferred edges ignore formatting-only coincidences in short outputs.

## [1.0.0] - 2022-12-06

### Added

- Stable CLI contract for graph, taint, verdict, and version, exit codes 0/1/2.
- Tests pin the taint chain across the bundled traces.

## [0.9.5] - 2021-05-11

### Changed

- Maintenance release: documentation pass and fixture refresh.

## [0.9.0] - 2020-10-27

### Added

- Reason chains record whether each hop was declared or inferred.

## [0.8.0] - 2019-07-23

### Added

- Clean and contaminated trace fixtures.
- README walkthrough captured from a real run.

## [0.7.0] - 2018-11-06

### Added

- Test suite covering the parser, the graph, taint, and the CLI.

## [0.6.0] - 2017-03-14

### Added

- Report renderer with stable finding lines.
- CLI entry point with subcommands.

## [0.5.0] - 2016-06-28

### Added

- Verdicts: grounded, tainted, unknown.

## [0.4.0] - 2015-09-08

