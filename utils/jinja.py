from jinja2 import Template


def render_template(html: str, **kwargs: ...) -> str:
    template = Template(html)
    return template.render(**kwargs)
