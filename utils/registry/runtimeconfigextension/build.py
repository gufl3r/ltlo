import pyglet
import game.entitymodels.generic as generic_entities
import game.entitymodels.menu as menu_entities
import copy

def build(cfg: dict):
    def button_distances(entities: list) -> dict:
        rect_idx = None
        label_idx = None

        for i, ent in enumerate(entities):
            obj = ent.drawable  # ajuste se o atributo tiver outro nome

            if rect_idx is None and isinstance(obj, pyglet.shapes.RoundedRectangle):
                rect_idx = i

            if label_idx is None and isinstance(obj, pyglet.text.Label):
                label_idx = i

            if rect_idx is not None and label_idx is not None:
                break

        if rect_idx is None or label_idx is None:
            raise ValueError("rect ou label nao encontrado na lista")

        return {
                "rect_to_label": abs(rect_idx - label_idx)
        }
    def numeric_stepper_distances(entities: list) -> dict:
        decrease_idx = None
        value_idx = None
        increase_idx = None

        for i, ent in enumerate(entities):
            tags = getattr(ent, "tags", [])

            if "numeric_stepper" not in tags:
                continue

            if "decrease" in tags and decrease_idx is None:
                decrease_idx = i
            elif "increase" in tags and increase_idx is None:
                increase_idx = i
            elif value_idx is None:
                value_idx = i

            if decrease_idx is not None and value_idx is not None and increase_idx is not None:
                break

        if decrease_idx is None or value_idx is None or increase_idx is None:
            raise ValueError("numeric_stepper incompleto na lista de entidades")

        return {
                "decrease_to_value": value_idx - decrease_idx,
                "increase_to_value": value_idx - increase_idx,
        }
    new_cfg = copy.deepcopy(cfg)
    button = generic_entities.button("test","test",(100,100),(100,100),(100,100,100),(100,100,100,100),100,100,None)
    numeric_stepper = menu_entities.numeric_stepper(
        name="test",
        value_text="test",
        position=(100,100),
        size=(100,100),
        background_color=(100, 100, 100),
        text_color=(100, 100, 100, 100),
        text_size=100,
        duration=100,
        hud=False,
        tags=[f"domain:"]
    )
    ui_offsets = {
        "numeric_stepper": numeric_stepper_distances(numeric_stepper),
        "button": button_distances(button)
    }
    new_cfg["ui"]["offsets"] = ui_offsets

    return new_cfg