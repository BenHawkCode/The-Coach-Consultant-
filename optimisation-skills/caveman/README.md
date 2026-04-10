# Caveman - Output Token Compression

Reduces Claude's output tokens by ~65-75% while maintaining technical accuracy.

## Installation

Already installed as a Claude Code plugin:
```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

## Usage

```
/caveman          # Default mode (~65% reduction)
/caveman lite     # Light - removes filler, keeps grammar
/caveman full     # Default - drops articles, fragments
/caveman ultra    # Maximum compression, telegraphic style
stop caveman      # Return to normal mode
```

## How It Fits

| Tool | What It Reduces | Savings |
|------|----------------|---------|
| Token Optimisation | Input tokens (CLAUDE.md, skill files) | ~40% on context |
| Caveman | Output tokens (Claude's responses) | ~65-75% on output |

Both tools together = significant cost reduction per conversation.

## Source

GitHub: https://github.com/JuliusBrussee/caveman
