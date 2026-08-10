---
title: Markdown Exporter
author: Bowen Liang
---

# Introduction

## Welcome Slide

Welcome to our Markdown Exporter!

::: notes
Remember to greet the audience warmly.
:::

---

# Section 1: Basic Layouts

## Title and Content

- This is a basic slide with bullet points
- It uses the "Title and Content" layout
- Perfect for simple content presentation

## Two Column Layout

::::: columns
::: column
Left column content:
- Point 1
- Point 2
:::
::: column
Right column content:
- Point A
- Point B
:::
:::::

## Comparison Layout

::::: columns
::: column
Text followed by an image:

![Test Image](https://avatars.githubusercontent.com/u/127165244?s=48&v=4)
:::
::: column
- This triggers the "Comparison" layout
- Useful for side-by-side comparisons
:::
:::::

## Content with Caption

Here's some explanatory text about the image below.

![Test Image](https://avatars.githubusercontent.com/u/127165244?s=48&v=4 "fig:Test Image")

---

# Section 2: Advanced Features

## Code Block

Here's a Python code block:

```python
def greet(name):
    return f"Hello, {name}!"


print(greet("World"))
```

## Table Example

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1    | Data     | More     |
| Row 2    | Info     | Stuff    |

## Incremental List

::: incremental
- This point appears first
- Then this one
- And finally this one
:::

## {background-image="https://avatars.githubusercontent.com/u/127165244?s=48&v=4"}

::: notes
This is a slide with a background image and speaker notes only.
The "Blank" layout will be used.
:::

# Conclusion

## Thank You

Thank you for viewing this kitchen sink presentation!

::: notes
Remember to thank the audience and invite questions.
:::