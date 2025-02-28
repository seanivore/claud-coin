# Contributing to $CLAUD Coin

First off, thank you for considering contributing to $CLAUD Coin! It's people like you that make this project a great tool for the AI development community. This document provides guidelines and steps for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](https://github.com/seanivore/claud-coin/blob/claud-coin/CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for $CLAUD Coin.

Before creating bug reports, please check [the issue list](https://github.com/seanivore/claud-coin/issues) as you might find that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title** for the issue
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and/or animated GIFs** if possible
* **Include details about your environment**

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for $CLAUD Coin, including completely new features and minor improvements to existing functionality.

* **Use a clear and descriptive title** for the issue
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps or point out the affected parts**
* **Describe the current behavior and explain why a change would be beneficial**
* **Explain why this enhancement would be useful to most users**

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible
* Follow the Rust style guidelines
* Include thoughtfully-worded, well-structured tests
* Document new code
* End all files with a newline

## Development Setup

To set up for development:

1. Fork the repository
2. Clone your fork to your local machine
3. Install Rust and Cargo if you haven't already
4. Set up the Solana development environment:
   ```
   sh -c "$(curl -sSfL https://release.solana.com/v1.14.11/install)"
   ```
5. Install project dependencies:
   ```
   cargo build
   ```
6. Run the test suite to ensure everything is working:
   ```
   cargo test
   ```

## Style Guidelines

### Rust Code

Follow the official [Rust style guidelines](https://doc.rust-lang.org/1.0.0/style/). We also use:

* `rustfmt` for code formatting
* `clippy` for linting

Run these tools before submitting PRs:
```
cargo fmt
cargo clippy
```

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
  * 🎨 when improving the format/structure of the code
  * 🐎 when improving performance
  * 🚱 when plugging memory leaks
  * 📝 when writing docs
  * 🐛 when fixing a bug
  * 🔥 when removing code or files
  * 💚 when fixing CI builds
  * ✅ when adding tests
  * 🔒 when dealing with security

## Questions?

Feel free to reach out to the project maintainers for any questions about contributing!