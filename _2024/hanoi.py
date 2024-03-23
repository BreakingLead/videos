from manim import *


def c_tex(s: str, *ts, **kw) -> Tex:
    return Tex(
        s,
        tex_template=TexTemplateLibrary.ctex,
        font_size=144,
    )


class Intro(Scene):
    n = 10

    def construct(self):
        p_a = Rectangle(GRAY_B, height=5, width=0.3)
        p_b = Rectangle(GRAY_B, height=5, width=0.3)
        p_c = Rectangle(GRAY_B, height=5, width=0.3)

        p_a.set_fill(GRAY_C, opacity=0.8)
        p_b.set_fill(GRAY_C, opacity=0.8)
        p_c.set_fill(GRAY_C, opacity=0.8)

        pillars = VGroup(p_a, p_b, p_c).arrange(buff=4)

        vg = VGroup()
        _t = []
        colors = color_gradient([RED, GREEN, BLUE], self.n)
        for i in range(self.n):
            rect = RoundedRectangle(
                corner_radius=0.05, color=GRAY_D, height=0.3, width=(self.n - i) * 0.4
            )
            rect.set_fill(colors[i], opacity=1.0)
            vg += rect
            _t.append(rect)

        vg.move_to(p_a.get_bottom() + UP * 0.15).arrange(UP, buff=0, center=False)

        l_dict = {
            "a": _t,
            "b": [],
            "c": [],
        }

        pillars_dict = {
            "a": p_a,
            "b": p_b,
            "c": p_c,
        }

        self.play(DrawBorderThenFill(pillars))
        self.play(Create(vg))
        self.wait(3)

        op_list = self.mv(self.n)

        def mov(op: str):
            rt = 0.15
            f = op[0]
            t = op[1]
            now = l_dict[f].pop()
            self.play(now.animate.move_to(pillars_dict[f].get_top() + UP), run_time=rt)
            self.play(now.animate.move_to(pillars_dict[t].get_top() + UP), run_time=rt)
            self.play(
                now.animate.move_to(
                    pillars_dict[t].get_bottom() + 0.3 * UP * len(l_dict[t]) + 0.15 * UP
                ),
                run_time=rt,
            )
            l_dict[t].append(now)

        for op in op_list:
            mov(op)

    @staticmethod
    def mv(x):
        res = []

        def f(k, a, b, c):
            if k == 1:
                res.append(f"{a}{c}")
            else:
                f(k - 1, a, c, b)
                res.append(f"{a}{c}")
                f(k - 1, b, a, c)

        f(x, "a", "b", "c")
        return res
