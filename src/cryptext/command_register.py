from .commands import Ls, Cat, Touch, Mkdir, Rm, Cd, Exit


class Register:
    class UnknownModeError(Exception):
        pass

    @staticmethod
    def register(registry, mode: str) -> None:
        if mode not in 'rw' and mode != 'wr':
            raise (Register.UnknownModeError(f'Mode {mode!r} is unknown.'))
        if 'r' in mode:
            Register._register_read_only(registry)
        if 'w' in mode:
            Register._register_write(registry)

    @staticmethod
    def _register_read_only(registry) -> None:
        registry.register(Ls)
        registry.register(Cat)
        registry.register(Cd)
        registry.register(Exit)

    @staticmethod
    def _register_write(registry) -> None:
        registry.register(Touch)
        registry.register(Mkdir)
        registry.register(Rm)
