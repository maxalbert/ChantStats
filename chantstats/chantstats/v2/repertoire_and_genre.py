from .utils import EnumWithDescription

__all__ = ["RepertoireAndGenreType"]


class RepertoireAndGenreType(EnumWithDescription):
    PLAINCHANT_SEQUENCES = ("plainchant_sequences", "Sequences", ("chant", "sequences"), ("Chant: ", "Seq.: "))
    RESPONSORIAL_CHANTS = (
        "responsorial_chants",
        "Responsorial Chants",
        ("chant", "responsorial_chants"),
        ("Chant: ", "Resp.: "),
    )
    ORGANA = ("organa", "Organa", ("organum", ""), ("Organum: ", ""))

    def __new__(cls, name, desc, output_path_stubs, plot_title_descr, **kwargs):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj._description = desc
        obj.output_path_stub_1 = output_path_stubs[0]
        obj.output_path_stub_2 = output_path_stubs[1]
        obj.plot_title_descr_1 = plot_title_descr[0]
        obj.plot_title_descr_2 = plot_title_descr[1]
        return obj
