from manim import *
from functools import reduce
from manim.camera.camera import Camera

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# from manim_voiceover.services.recorder import RecorderService


def segment(start, end, **kwargs):
    line = Line(start, end, **kwargs)
    line.add(Dot(start, **kwargs), Dot(end, **kwargs))
    return line


def is_max_of_list(x, nums: List):
    return max(nums) == x


def color_for_arg(x, fn, nums):
    ys = [fn(i) for i in nums]
    if all(abs(elem - ys[0]) < 0.001 for elem in ys):
        return ORANGE
    else:
        return RED if is_max_of_list(fn(x), ys) else BLUE


class Cover(Scene):
    def construct(self):
        if "Cover":
            # self.camera.background_color = ManimColor.from_rgb("#093145")

            title_1 = MathTex(
                r"b,c \in {\mathbb{R}},\forall x \in \lbrack 0,4\rbrack \\ \left| x^{2} - bx - c \right| \leq M",
                font_size=70,
            )
            title_2 = Text("M 的最小值为？")
            title_3 = Text("初中生也能秒了?", color=YELLOW)

            self.add(VGroup(title_1, title_2, title_3).arrange(DOWN))


class P0(VoiceoverScene):
    def construct(self):
        if True:
            problem = MathTex(
                r"b,c \in {\mathbb{R}},\forall x \in \lbrack 0,4\rbrack \left|x^{2}-bx-c\right|\leq M",
            ).scale_to_fit_width(config.frame_width - 1)

            p1 = Text("求 M 的最小值")
            ps = VGroup(problem, p1).arrange(DOWN)

            pt = MathTex(r"\left|x^{2} + bx + c \right| \leq M")

            self.play(Write(ps))
            self.wait(1)
            self.play(Transform(ps, pt))
            self.wait(1)

            pt1 = MathTex(
                r"f(x) = x^2 + bx + c",
            ).next_to(ps, DOWN)
            ps.add(pt1)

            self.play(Write(pt1))
            self.play(FadeOut(ps))


class P1(Scene):
    def construct(self):
        if True:
            """
            我们在初中就已经学过
            """

            nump = NumberPlane(
                x_range=[-8, 8, 1],
                y_range=[-4, 16, 2],
                x_length=(128.0 / 9.0),
                y_length=8,
                axis_config={"include_ticks": False, "include_numbers": True},
            )
            origin = Dot(nump.c2p(0, 0))

            a = ValueTracker(1)
            b = ValueTracker(0)
            c = ValueTracker(0)
            h = ValueTracker(0)
            v = ValueTracker(0)

            def f(x) -> float:
                return (
                    a.get_value() * ((x - h.get_value()) ** 2)
                    + b.get_value() * (x - h.get_value())
                    + c.get_value()
                    + v.get_value()
                )

            graph = always_redraw(lambda: nump.plot(f, color=YELLOW_C))

            label = nump.get_graph_label(
                graph=graph, label="{{a}} x^2 + {{b}} x + {{c}}"
            )

            text_a = Text("")
            text_b = Text("")
            text_c = Text("")
            text_params_abc = VGroup(text_a, text_b, text_c)
            text_a.add_updater(
                lambda m: m.become(
                    MathTex(f"a = {a.get_value():.1f}"), match_center=True
                )
            )
            text_b.add_updater(
                lambda m: m.become(
                    MathTex(f"b = {b.get_value():.1f}"), match_center=True
                )
            )
            text_c.add_updater(
                lambda m: m.become(
                    MathTex(f"c = {c.get_value():.1f}"), match_center=True
                )
            )

            text_params_abc.add_updater(lambda m: m.arrange(DOWN).next_to(label, DOWN))

            self.add(origin)
            self.play(Create(nump), Write(graph), Write(label))

            """
            a 控制开口大小, b 和 c 共同控制图像的上下左右平移
            """

            self.play(Write(text_params_abc))
            self.play(a.animate.set_value(-1), rate_func=rate_functions.linear)
            self.play(a.animate.set_value(1), rate_func=rate_functions.linear)
            self.wait(1)

            self.play(b.animate.set_value(-3), run_time=3)
            self.play(b.animate.set_value(3), run_time=3)
            self.play(b.animate.set_value(0), run_time=3)
            self.wait(1)

            self.play(c.animate.set_value(-3))
            self.play(c.animate.set_value(3))
            self.play(c.animate.set_value(0))

            self.play(Uncreate(text_a), Uncreate(text_b), Uncreate(text_c))
            self.wait(1)
            l2 = lambda: "a (x-({:.1f}))^2 + b (x-({:.1f})) + c {:+.1f}".format(
                h.get_value(),
                h.get_value(),
                v.get_value(),
            )
            label2 = always_redraw(lambda: MathTex(l2()).to_corner())

            self.play(TransformMatchingTex(label, label2))

            """
            因此我们平移这个函数之后， a 的值不会改变
            """

            self.play(h.animate.set_value(-2))
            self.play(h.animate.set_value(2))
            self.play(h.animate.set_value(0))
            self.play(v.animate.set_value(4))
            self.play(v.animate.set_value(-4))
            self.play(v.animate.set_value(0))


class P2(Scene):
    time_scale = 1

    def construct(self):
        if True:

            def func(x) -> float:
                return x**2

            nump = NumberPlane(
                x_range=[-8, 8, 1],
                y_range=[-4, 16, 2],
                x_length=(128.0 / 9.0),
                y_length=8,
                axis_config={"include_ticks": False, "include_numbers": True},
            )
            origin = Dot(nump.c2p(0, 0))
            graph = nump.plot(func, color=YELLOW_C)
            label = nump.get_graph_label(
                graph=graph, label="{{a}} x^2 + {{b}} x + {{c}}"
            )

            numpg = VGroup(nump, graph, label, origin)

            self.add(numpg)

            h = ValueTracker(0)
            v = ValueTracker(0)
            a = ValueTracker(1)
            b = ValueTracker(0)
            c = ValueTracker(0)

            def func2(x) -> float:
                return abs(
                    a.get_value() * ((x - h.get_value()) ** 2)
                    + b.get_value() * (x - h.get_value())
                    + c.get_value()
                    + v.get_value()
                )

            nump2 = Axes(
                x_range=[-1, 5, 1],
                y_range=[-4, 22, 2],
                x_length=(128.0 / 9.0) * 0.5,
                y_length=8,
                axis_config={"include_ticks": False, "include_numbers": True},
            )

            origin2 = Dot(nump2.c2p(0, 0))
            numpg2 = VGroup(nump2, origin2).shift(LEFT * 2.2)

            self.play(Transform(numpg, numpg2))

            graph2 = always_redraw(lambda: nump2.plot(func2, color=YELLOW))
            # TODO: Replace H, V as values
            label2 = nump2.get_graph_label(
                graph=graph2, label=r"\left| (x-H)^2+(x-H)+V \right|"
            )

            text_h = Tex(f"H = {h.get_value():.1f}").next_to(label2, DOWN)
            text_v = Tex(f"V = {v.get_value():.1f}").next_to(text_h, DOWN)
            text_h.add_updater(
                lambda mob: mob.become(
                    Text(f"H = {h.get_value():.1f}"), match_center=True
                )
            )
            text_v.add_updater(
                lambda mob: mob.become(
                    Text(f"V = {v.get_value():.1f}"), match_center=True
                )
            )

            def mid():
                return -(b.get_value() / (2 * a.get_value())) + h.get_value()

            graph2_mid_dot = always_redraw(lambda: Dot(nump2.c2p(mid(), func2(mid()))))

            self.play(Write(graph2), Write(label2), Write(text_h), Write(text_v))

            graph2_l = always_redraw(lambda: nump2.get_T_label(0, graph2))
            graph2_r = always_redraw(lambda: nump2.get_T_label(4, graph2))

            r = [0, 4]
            graph2_vl = always_redraw(
                lambda: nump2.plot(
                    lambda x: func2(0), color=color_for_arg(0, func2, r)
                ).set_stroke(width=10)
            )
            graph2_vr = always_redraw(
                lambda: nump2.plot(
                    lambda x: func2(4), color=color_for_arg(4, func2, r)
                ).set_stroke(width=10)
            )

            self.play(
                Write(graph2_l), Write(graph2_r), Write(graph2_vl), Write(graph2_vr)
            )

            self.add(graph2_mid_dot)

            """
            由图像左右平移的表现不难看出，在图像高度不变的情况下，当且仅当f(0)＝f(2)时，f(x)在区间的最大值最小，不管左移或右移，都会令一端大于另一端，从而导致最大值变大，我们就找到了H的取值。
            """
            self.play(
                h.animate.set_value(4),
                rate_func=rate_functions.linear,
                run_time=6 * self.time_scale,
            )
            self.play(
                h.animate.set_value(0),
                rate_func=rate_functions.linear,
                run_time=6 * self.time_scale,
            )
            self.wait(1)

            self.play(h.animate.set_value(2), run_time=2 * self.time_scale)

            graph2_vm = always_redraw(
                lambda: nump2.plot(
                    lambda x: func2(mid()), color=color_for_arg(mid(), func2, r)
                ).set_stroke(width=10)
            )

            self.play(Write(graph2_vm))

            r.append(mid())

            """
            那么我们想要找到V的取值，
            只需要让f(x)的最值等于V取0时的一半即可，
            此时三个最大值相等，
            我们就找到了这三个最大值最小的位置。
            """

            self.play(v.animate.set_value(-5), run_time=5 * self.time_scale)
            self.wait(1)
            self.play(v.animate.set_value(5), run_time=5 * self.time_scale)
            self.wait(1)
            self.play(v.animate.set_value(-2), run_time=3 * self.time_scale)
            self.wait(1)

            text_m_min = Text("M的最小值为2").next_to(graph2_vm)
            self.play(Write(text_m_min))
            self.wait(1)

            now_all = VGroup(
                graph2,
                graph2_l,
                graph2_r,
                graph2_vl,
                graph2_vm,
                graph2_vr,
                graph2_mid_dot,
                text_h,
                text_v,
                nump2,
                text_m_min,
                origin2,
                numpg2,
                nump,
                numpg,
            )

            """
            此时我们已经找到了函数值最大值的最小值，但我们也可以顺手求出b和c的值，只需要将平移后的函数展开即可。
            """
            ans_1 = MathTex(r"\left| (x-2)^2+(x-2)-2 \right|").center().shift(3 * UP)

            # 16
            self.play(FadeOut(now_all))
            self.play(Transform(label2, ans_1))

            ans_2 = MathTex(
                r"""
                &= \left| x^2 - 2x + 4 + x - 2 - 2\right| \\
                &= \left| x^2 - x \right| \\
                & \Rightarrow b = 1, c = 0
                """
            ).next_to(ans_1, DOWN)

            ans_3 = Tex(
                "此时", "$M_{\min} = 2$", tex_template=TexTemplateLibrary.ctex
            ).next_to(ans_2, DOWN)

            self.play(Write(ans_2), run_time=4)
            self.play(Write(ans_3))
            self.wait(2)
            self.clear()

            text_sp = Text("证明？").center()

            self.play(Write(text_sp))
            self.wait(1)


class P3(Scene):
    def construct(self):
        config.tex_template = TexTemplateLibrary.ctex
        text_sp = Text("证明？").center()
        self.play(Write(text_sp))
        self.wait(1)

        """
        我们知道一般用不严谨的方法求出了答案，就可以用反证法验证答案的准确性。
        """
        self.play(Transform(text_sp, Text("反证法！").center()))
        self.play(text_sp.animate.to_corner(UL))

        tex1 = (
            Tex(
                r"要证明的命题: $b,c \in {\mathbb{R}},\forall x \in \lbrack 0,4\rbrack$ \\",
                r"$\left| x^{2} - bx - c \right| \leq M, M_{\min} = 2$",
            )
            .move_to(text_sp)
            .align_to(text_sp, LEFT)
        )
        self.play(Transform(text_sp, tex1))

        tex2 = (
            Tex(r"即$f(x) = \left|x^2-bx-c\right|, (f(x)_{\max})_{\min} = 2$")
            .next_to(text_sp, DOWN)
            .align_to(text_sp, LEFT)
        )
        self.play(Write(tex2))
        self.wait()

        tex3 = (
            Tex(r"反证法: 令 $(f(x)_{\max})_{\min} < 2$")
            .next_to(tex2, DOWN)
            .align_to(tex2, LEFT)
        )
        self.play(Write(tex3))
        self.wait()

        tex4 = (
            Tex(
                r"""$$
                \begin{cases}
                f(0) = -c      &< 2 \framebox{A}\\
                f(2) = 4-2b-c  &< 2 \framebox{B}\\
                f(4) = 16-4b-c &< 2 \framebox{C}
                \end{cases}
                $$"""
            )
            .next_to(tex3, DOWN)
            .align_to(tex3, LEFT)
        )
        self.play(Write(tex4))
        self.wait()

        tex5 = (
            Tex(
                r"""\[
                \begin{aligned}
                \framebox{A} \Rightarrow c > -2 \\
                \framebox{C} - 2 \framebox{B} \Rightarrow 8 + c < -2 \\
                \Rightarrow c < -10
                \end{aligned}
                \]"""
            )
            .next_to(tex4, RIGHT)
            .align_to(tex4, UP)
        )
        self.play(Write(tex5))

        g_temp = VGroup(tex3, tex4, tex5)

        tex6 = Tex(
            r"矛盾! 故 $(f(x)_{\max})_{\min} \geq 2$ \\",
            r"当且仅当 $b=1,c=0$ 时等号成立，此时$(f(x)_{\max})_{\min} = 2$",
        ).center()
        self.play(Transform(g_temp, tex6))

        self.wait()


class P4(Scene):
    def construct(self):
        config.tex_template = TexTemplateLibrary.ctex

        text1 = Text("能不能再给力一点? ")
        text2 = Text("从特殊到一般", t2c={"[1:3]": YELLOW, "[4:]": YELLOW})
        vg1 = VGroup(text1, text2).arrange(DOWN)

        self.play(Write(text1))
        self.wait()
        self.play(Write(text2))
        self.wait()
        self.play(FadeOut(vg1))

        tex1 = Tex(
            r"$ f(x) = x^2 + bx + c $",
            r"求 $ \left|f(x)\right| $",
            r"在 $ \lbrack L, R \rbrack $ 上最大值的最小值。",
        )

        self.play(Write(tex1))
        self.wait()

        h = ValueTracker(0)
        v = ValueTracker(0)
        a = ValueTracker(1)
        b = ValueTracker(0)
        c = ValueTracker(0)
        l = ValueTracker(1.5)
        offset = ValueTracker(2)

        def fn(x) -> float:
            return (
                a.get_value() * ((x - h.get_value()) ** 2)
                + b.get_value() * (x - h.get_value())
                + c.get_value()
                + v.get_value()
            )

        def mid():
            return -(b.get_value() / (2 * a.get_value())) + h.get_value()

        ax = NumberPlane(
            axis_config={"include_ticks": False, "include_numbers": True},
        )

        mid_dot = always_redraw(lambda: Dot(ax.c2p(mid(), abs(fn(mid())))))
        graph = always_redraw(lambda: ax.plot(lambda x: abs(fn(x)), [-8, 8]))

        line_l = always_redraw(
            lambda: ax.plot_line_graph(
                [l.get_value(), l.get_value()], [-10, 10], add_vertex_dots=False
            )
        )
        line_r = always_redraw(
            lambda: ax.plot_line_graph(
                [
                    l.get_value() + offset.get_value(),
                    l.get_value() + offset.get_value(),
                ],
                [-10, 10],
                add_vertex_dots=False,
            )
        )

        vg_lr = VGroup(line_l, line_r)
        origin = Dot(ax.c2p(0, 0))

        line_offset = always_redraw(
            lambda: ax.plot_line_graph(
                [l.get_value(), l.get_value() + offset.get_value()], [-2, -2]
            )
        )
        text_offset = always_redraw(
            lambda: BraceLabel(
                line_offset, r"R-L = {:.1f}".format(offset.get_value()), color=YELLOW
            )
        )
        self.play(Create(ax), Create(origin), tex1.animate.to_corner(UL))
        self.play(Write(graph), Create(mid_dot))
        self.play(Write(vg_lr), Write(line_offset), Write(text_offset))

        """
        我们发现
        只要区间长度R-L不变，那么我们要求的这个值的大小就不会改变。
        """
        self.play(h.animate.set_value(l.get_value() + offset.get_value() / 2))
        self.play(v.animate.set_value(-fn(l.get_value()) / 2))
        self.wait()
        self.play(h.animate.set_value(0), v.animate.set_value(0))

        self.play(l.animate.set_value(-3))

        self.play(h.animate.set_value(l.get_value() + offset.get_value() / 2))
        self.play(v.animate.set_value(-fn(l.get_value()) / 2))
        self.wait()
        self.play(h.animate.set_value(0), v.animate.set_value(0))

        self.play(l.animate.set_value(-1.5))

        self.play(h.animate.set_value(l.get_value() + offset.get_value() / 2))
        self.play(v.animate.set_value(-fn(l.get_value()) / 2))
        self.wait()
        self.play(h.animate.set_value(0), v.animate.set_value(0))

        """
        所以，我们不妨直接令这个区间固定关于y轴对称，将区间的平移转换成函数的平移，就容易推出通解。
        """
        self.play(l.animate.set_value(offset.get_value() / (-2)))

        self.play(offset.animate.set_value(3), l.animate.set_value(3 / (-2)))

        self.play(h.animate.set_value(l.get_value() + offset.get_value() / 2))
        self.play(v.animate.set_value(-fn(l.get_value()) / 2))
        self.wait()
        self.play(h.animate.set_value(0), v.animate.set_value(0))

        self.play(offset.animate.set_value(4), l.animate.set_value(4 / (-2)))

        self.play(h.animate.set_value(l.get_value() + offset.get_value() / 2))
        self.play(v.animate.set_value(-fn(l.get_value()) / 2))
        self.wait()
        self.play(h.animate.set_value(0), v.animate.set_value(0))

        tex2 = MathTex(
            r"((\left|f(x)\right|)_{\max})_{\min} = \dfrac{1}{2}\left( \dfrac{(R-L)}{2} \right)^2"
        ).to_corner()
        self.wait()

        self.play(
            Write(tex2),
            Uncreate(
                VGroup(
                    ax,
                    graph,
                    mid_dot,
                    origin,
                    vg_lr,
                    line_l,
                    line_r,
                    line_offset,
                    text_offset,
                )
            ),
        )
        self.play(tex2.animate.center())
        self.wait()

        self.play(Unwrite(tex1), Transform(tex2, Text("还能不能再给力一点？？")))

        self.wait()


class P5(Scene):
    def construct(self):
        config.tex_template = TexTemplateLibrary.ctex

        self.add(text1 := Text("还能不能再给力一点？？"))  # 继续推广
        self.play(
            Write(
                text2 := Tex(
                    r"对于任意 $g(x) = \left| f(x)  -bx-c \right|$",
                    r"求 $(g(x)_{\max})_{\min} , x \in [L,R]$ ?",
                ).next_to(text1, DOWN)
            )
        )
        self.wait(3)

        """先从特殊入手，再推出一般结论"""
        self.play(
            Transform(
                text2,
                text3 := Tex(
                    r"例: $f(x) = \left| x + \frac{1}{x} - bx - c \right|$"
                    r"求 $f(x)$ 在 $\lbrack \frac{1}{2} , 2 \rbrack$ \\上最大值的最小值",
                ).to_edge(UP),
            ),
            Unwrite(text1),
        )

        """
        即使函数的极值点发生偏移，但其实并不影响最大值的最小值的取值情况。
        只要满足上文得出的结论:|f(x)|在区间两端点的函数值相等，且等于中间隆起的最大值，
        就可以得到我们所要求的这个最大值的最小值。
        """
        b = ValueTracker(0.2)
        c = ValueTracker(0)

        def fn(x: float) -> float:
            return abs(x + (1.0 / x) - b.get_value() * x - c.get_value())

        ax = Axes(
            [0, 4, 0.5],
            [0, 4, 0.25],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True},
        ).to_corner(DL)
        g = always_redraw(lambda: ax.plot(lambda x: abs(fn(x)), [0.2, 4]))
        ll = always_redraw(lambda: ax.get_T_label(0.5, g))
        lr = always_redraw(lambda: ax.get_T_label(2, g))

        r = [0.5, 2, 1]
        graph2_vl = always_redraw(
            lambda: ax.plot(
                lambda x: fn(0.5), color=color_for_arg(0.5, fn, r)
            ).set_stroke(width=3)
        )
        graph2_vm = always_redraw(
            lambda: ax.plot(lambda x: fn(1), color=color_for_arg(1, fn, r)).set_stroke(
                width=3
            )
        )
        graph2_vr = always_redraw(
            lambda: ax.plot(lambda x: fn(2), color=color_for_arg(2, fn, r)).set_stroke(
                width=3
            )
        )

        self.play(
            Create(ax),
            Create(g),
            Create(ll),
            Create(lr),
            Write(graph2_vl),
            Write(graph2_vr),
            Write(graph2_vm),
        )
        self.wait(2)
        self.play(b.animate.set_value(0), c.animate.set_value(2.25), run_time=4)

        self.play(
            Write(
                text4 := MathTex(
                    r"f(0.5) = f(2) \Rightarrow b &= 0 \\"
                    r"\text{求导可得极值点为} 1 \Rightarrow -f(1) = f(2) \Rightarrow c &= 2.25 \\"
                    r"\text{此时} f(0.5) = f(1) = f(2) = 0.25"
                ).next_to(text3, DOWN)
            ),
            run_time=6,
        )

        self.wait(2)


class P6(Scene):
    def construct(self):
        config.tex_template = TexTemplateLibrary.ctex
        text1 = Tex(
            r"1. 已知\(f(x) = \left| x^{3} + bx + c \right|\), \\求其在\(\lbrack - 5,2\rbrack\)中最大值的最小值"
        )
        text2 = Tex(
            r"2. 已知\(F(x) = \left| \left( \frac{1}{4} \right)x^{3} - x^{2} - a \right|\),\\求\(F(x)\)在\(\lbrack - 2,4\rbrack\)的最大值的最小值（2019北京卷）"
        )
        vg = VGroup(text1, text2).arrange(DOWN, buff=2)
        self.play(Write(vg), run_time=4)
