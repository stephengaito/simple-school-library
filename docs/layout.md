# Html Layout

I want a basic HTML based layout:


```
----------------------
|       header       |
|--------------------|
|      mainMenu      |
|--------------------|
|         |          |
| subMenu | content  |
|         |          |
|--------------------|
|       footer       |
----------------------
```

with a 20% / 80% split between the `submenu` and `content` columns

See: 
  - [HTML Layout - GeeksforGeeks](https://www.geeksforgeeks.org/html-layout/)
  - [HTML Semantic Elements](https://www.w3schools.com/html/html5_semantic_elements.asp)

We will do this using semantic HTML elements

- `<header>`
- `<nav>` which contains the top level menu (`mainMenu`)
- `<main>` which contains the `submenu` / `content` columns
- `<aside>` which contains the `submenu`
- `<section>` which contains the `content`
- `<footer>`

which are styled using CSS.

The `<main>` will be styled as a flex row container with two elements one
with a width of 20% and the other with a width of 80%.

The `<aside>` and the `<section>` elements will be styles as flex columns.

To do this we will use [Tailwind CSS](https://tailwindcss.com/docs). In
particular we will use the

- [flex - Flexbox & Grid - Tailwind CSS](https://tailwindcss.com/docs/flex)
- [flex-direction - Flexbox & Grid - Tailwind CSS](https://tailwindcss.com/docs/flex-direction)
- [width - Sizing - Tailwind CSS](https://tailwindcss.com/docs/width)

classes.

## Resources

- [</> htmx ~ Documentation](https://htmx.org/docs/)
- [htmx multi-swap extension](https://github.com/bigskysoftware/htmx-extensions/blob/main/src/multi-swap/README.md)
- [How To Make a Breadcrumb Navigation](https://www.w3schools.com/howto/howto_css_breadcrumbs.asp)
- [</> htmx ~ Examples ~ Updating Other Content](https://htmx.org/examples/update-other-content/)
- [How to update 2 target with htmx? - Stack Overflow](https://stackoverflow.com/questions/76451723/how-to-update-2-target-with-htmx)

## ToDo

We would have to update the htmlPage to the new style, and then all
responses could oob-swap mainMenu or subMenu in addition to changing the
content.

This will take a lot of work hunting down old LevelXdiv's 

Alternatively we *could* simple change the current `grid` to `flex`.....

The semantic layout and oob-swap is probably the correct long term
solution.

