from shiny import App, render, ui, reactive, run_app

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_selectize(
            "books",
            "Books",
            choices=[
                "Genesis", "Exodus", "Leviticus", "Numeri", "Deuteronomium",
                "Josua", "Judices", "Samuel_I", "Samuel_II",
                "Reges_I", "Reges_II", "Jesaia", "Jeremia",
                "Ezechiel", "Hosea", "Joel", "Amos", "Obadia",
                "Jona", "Micha", "Nahum", "Habakuk", "Zephania",
                "Haggai", "Sacharia", "Maleachi", "Psalmi", "Iob",
                "Proverbia", "Ruth", "Canticum", "Ecclesiastes",
                "Threni", "Esther", "Daniel", "Esra", "Nehemia",
                "Chronica_I", "Chronica_II"
            ]
        ),
        ui.input_select(
            "scope",
            "Scope",
            choices=["book", "chapter", "verse", "sentence", "clause", "phrase"]
        ),
        ui.panel_conditional(
            "input.scope === 'sentence'",
            ui.h4("Sentence Features"),
            ui.input_select(
                "sentence_type",
                "Sentence Type",
                choices=[
                    "",
                    "AjCl", "CPen", "Defc", "Ellp", "InfA", "InfC", "MSyn", 
                    "NmCl", "Ptcp", "Reop", "Unkn", "Voct", "Way0", "WayX",
                    "WIm0", "WImX", "WQt0", "WQtX", "WxI0", "WXIm", "WxIX",
                    "WxQ0", "WXQt", "WxQX", "WxY0", "WXYq", "WxYX", "WYq0",
                    "WYqX", "xIm0", "XImp", "xImX", "XPos", "xQt0", "XQtl",
                    "xQtX", "xYq0", "XYqt", "xYqX", "ZIm0", "ZImX", "ZQt0",
                    "ZQtX", "ZYq0", "ZYqX"
                ]
            )
        ),
        ui.panel_conditional(
            "true",
            ui.h4("Word Features (all optional)"),
            ui.input_select(
                "sp",
                "Part of Speech",
                choices=[
                    "", "art", "verb", "subs", "nmpr", "advb", "prep", 
                    "conj", "prps", "prde", "prin", "intj", "nega",
                    "inrg", "adjv"
                ]
            ),
            ui.input_select(
                "gn",
                "Gender",
                choices=["", "m", "f", "NA", "unknown"]
            ),
            ui.input_select(
                "nu",
                "Number",
                choices=["", "sg", "du", "pl", "NA", "unknown"]
            ),
            ui.input_select(
                "ps",
                "Person",
                choices=["", "p1", "p2", "p3", "NA", "unknown"]
            ),
            ui.input_select(
                "st",
                "State",
                choices=["", "a", "c", "e"]
            ),
            ui.input_select(
                "vs",
                "Verbal Stem",
                choices=[
                    "", 
                    # Hebrew stems
                    "hif", "hit", "htpo", "hof", "nif", "piel", 
                    "poal", "poel", "pual", "qal",
                    # Aramaic stems
                    "afel", "etpa", "etpe", "haf", "hotp", "hsht",
                    "htpa", "htpe", "nit", "pael", "peal", "peil",
                    "shaf", "tif", "pasq"
                ]
            ),
            ui.input_select(
                "pdp",
                "Phrase Dependent Part of Speech",
                choices=[
                    "", "art", "verb", "subs", "nmpr", "advb", "prep", 
                    "conj", "prps", "prde", "prin", "intj", "nega",
                    "inrg", "adjv"
                ]
            ),
            ui.input_select(
                "prs_gn",
                "Pronominal Suffix Gender",
                choices=["", "m", "f", "NA", "unknown"]
            ),
            ui.input_select(
                "prs_nu",
                "Pronominal Suffix Number",
                choices=["", "sg", "du", "pl", "NA", "unknown"]
            ),
            ui.input_select(
                "prs_ps",
                "Pronominal Suffix Person",
                choices=["", "p1", "p2", "p3", "NA", "unknown"]
            ),
            ui.input_select(
                "ls",
                "Lexical Set",
                choices=[
                    "", "nmdi", "nmcp", "padv", "afad", "ppre", "cjad",
                    "ordn", "vbcp", "mult", "focp", "ques", "gntl",
                    "quot", "card", "none"
                ]
            ),
            ui.input_text(
                "gloss",
                "Gloss",
                placeholder="Enter gloss..."
            ),
        ),
    ),
    ui.card(
        ui.h3("Generated Query"),
        ui.tags.pre(
            ui.output_text("search_template"),
            style="white-space: pre; font-family: monospace;"
        ),
    )
)

def server(input, output, session):
    @render.text
    def search_template():
        features = []
        if input.sp():
            features.append(f"sp={input.sp()}")
        if input.gn():
            features.append(f"gn={input.gn()}")
        if input.nu():
            features.append(f"nu={input.nu()}")
        if input.ps():
            features.append(f"ps={input.ps()}")
        if input.st():
            features.append(f"st={input.st()}")
        if input.vs():
            features.append(f"vs={input.vs()}")
        if input.gloss():
            features.append(f"gloss={input.gloss()}")
        if input.pdp():
            features.append(f"pdp={input.pdp()}")
        if input.prs_gn():
            features.append(f"prs_gn={input.prs_gn()}")
        if input.prs_nu():
            features.append(f"prs_nu={input.prs_nu()}")
        if input.prs_ps():
            features.append(f"prs_ps={input.prs_ps()}")
        if input.ls():
            features.append(f"ls={input.ls()}")
            
        word_features = " ".join(features)
        sentence_type = f' typ="{input.sentence_type()}"' if input.scope() == "sentence" and input.sentence_type() else ""
        template = f"""query = \"\"\"
book book={input.books()}
  {input.scope()}{sentence_type}
    word{' ' + word_features if word_features else ''}
\"\"\""""
        return template

app = App(app_ui, server)
