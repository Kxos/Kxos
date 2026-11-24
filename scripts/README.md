# Script degli SVG del profilo

Generano le immagini in `assets/` (tema scuro e `-light`). Da eseguire dalla root del repo:

```sh
python scripts/gen_header.py assets    # header.svg, footer.svg (+ -light)
python scripts/gen_stack.py assets     # stack.svg, stack-it.svg (+ -light)
python scripts/gen_tagline.py assets   # tagline*.svg, badge-*.svg
```

Le categorie dello stack seguono ordine, numeri e colori della sezione Skills di kxos.github.io.
