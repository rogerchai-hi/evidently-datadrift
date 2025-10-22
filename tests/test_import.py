import importlib

import evidently


def get_undefined_alias() -> list[str]:
    TYPE_ALIASES = evidently.pydantic_utils.TYPE_ALIASES
    missing = []
    for alias, base_class in TYPE_ALIASES.items():
        module, attr = base_class.rsplit(".", 1)
        try:
            module_ = importlib.import_module(module)
            getattr(module_, attr)
        except (ModuleNotFoundError, AttributeError):
            missing.append(alias[1])
    return missing

def test_no_undefined_type_alias():
    assert len(get_undefined_alias()) == 0

if __name__ == "__main__":
    import pathlib
    import re

    missing = get_undefined_alias()
    root = pathlib.Path(__file__).resolve().parent.with_name("src")
    pattern = re.compile(r"^(?!.*#).*register_type_alias\([\s\S]*?\)", re.MULTILINE)

    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            define_str = match.group(0)
            for alias in missing:
                if alias in define_str:
                    print(f"{path.relative_to(root)} -> {alias}")
                    break