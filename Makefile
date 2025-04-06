.PHONY: all icons bootstrap clean

all: icons bootstrap htmx

STATIC_DIR=static
CSS_DIR=$(STATIC_DIR)/css
JS_DIR=$(STATIC_DIR)/js
FONTS_DIR=$(CSS_DIR)/fonts

BOOTSTRAP_ICONS_REPO=https://github.com/twbs/icons/raw/main/font
BOOTSTRAP_CSS=https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css
BOOTSTRAP_JS=https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js
JQUERY_JS=https://code.jquery.com/jquery-3.2.1.slim.min.js
POPPER_JS=https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js
HTMX_JS=https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js

ICONS_CSS=$(CSS_DIR)/bootstrap-icons.css
ICON_WOFF=$(FONTS_DIR)/bootstrap-icons.woff
ICON_WOFF2=$(FONTS_DIR)/bootstrap-icons.woff2
BOOTSTRAP_MIN_CSS=$(CSS_DIR)/bootstrap.min.css
BOOTSTRAP_MIN_JS=$(JS_DIR)/bootstrap.bundle.min.js

icons:
	@echo "Icons..."
	mkdir -p $(FONTS_DIR)
	wget -q -O $(ICONS_CSS) $(BOOTSTRAP_ICONS_REPO)/bootstrap-icons.css
	wget -q -O $(ICON_WOFF) $(BOOTSTRAP_ICONS_REPO)/fonts/bootstrap-icons.woff
	wget -q -O $(ICON_WOFF2) $(BOOTSTRAP_ICONS_REPO)/fonts/bootstrap-icons.woff2
	@echo "Downloaded $(CSS_DIR) and $(FONTS_DIR)"

htmx:
	@echo "HTMX..."
	mkdir -p $(JS_DIR)
	wget -q -O $(JS_DIR)/htmx.min.js $(HTMX_JS)
	wget -q -O $(JS_DIR)/jquery.min.js $(JQUERY_JS)
	wget -q -O $(JS_DIR)/popper.min.js $(POPPER_JS)
	@echo "Downloaded $(JS_DIR)"

bootstrap:
	@echo "Bootstrap..."
	mkdir -p $(CSS_DIR)
	mkdir -p $(JS_DIR)
	wget -q -O $(BOOTSTRAP_MIN_CSS) $(BOOTSTRAP_CSS)
	wget -q -O $(BOOTSTRAP_MIN_JS) $(BOOTSTRAP_JS)
	@echo "Downloaded $(CSS_DIR) and $(JS_DIR)"
