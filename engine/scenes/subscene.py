from pyglet.window import Window

import engine.scenes.scene as base_scene

import gc

class SubScene(base_scene.Scene):
    def __init__(self, window: Window, save: dict, data: dict) -> None:
        super().__init__(window, save)
        self.data: dict = data

    def dispose(self) -> None:
        protected_ids = set()

        def collect_ids(obj):
            protected_ids.add(id(obj))

            if isinstance(obj, dict):
                for v in obj.values():
                    collect_ids(v)
            elif isinstance(obj, (list, tuple, set)):
                for v in obj:
                    collect_ids(v)

        if hasattr(self, "data") and self.data is not None:
            collect_ids(self.data)

        # 2. Percorrer atributos da subscene
        for key, value in list(self.__dict__.items()):

            # nunca destruir window nem save
            if key in ("window", "save"):
                continue

            # se o objeto veio do data → só remover referência
            if id(value) in protected_ids:
                continue

            # tentar liberar recursos
            for method_name in ("delete", "dispose", "close", "release"):
                method = getattr(value, method_name, None)
                if callable(method):
                    try:
                        method()
                    except Exception:
                        pass

        # 3. Limpar apenas referências
        self.__dict__.clear()

        gc.collect()