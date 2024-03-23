from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex


class Cover(Scene):
    def construct(self):
        vg_t = VGroup(
            t1 := Text("柯西不等式的五种证明"),
            t2 := Tex(
                r"\[\left( \sum_{i = 1}^{n}a_{i}^{2} \right)\left( \sum_{i = 1}^{n}b_{i}^{2} \right) \geq \left( \sum_{i = 1}^{n}a_{i}b_{i} \right)^{2}\]"
            ),
        ).arrange(DOWN)

        self.play(Write(vg_t))
        self.wait()
        self.play(Unwrite(vg_t))


class Geo(VectorScene):
    def construct(self):
        t1 = Text("(1) 几何意义法")
        t2 = Tex(
            r"\[\left( \sum_{i = 1}^{n}a_{i}^{2} \right)\left( \sum_{i = 1}^{n}b_{i}^{2} \right) \geq \left( \sum_{i = 1}^{n}a_{i}b_{i} \right)^{2}\]"
        )

        vg1 = VGroup(t1, t2).arrange(DOWN)

        self.play(Write(vg1))

        self.wait()

        self.play(Unwrite(vg1))

        t3 = Tex(
            r"""
            Open the sum:
\[\left( a_{1}^{2} + a_{2}^{2} + \ldots + a_{n}^{2} \right)\left( b_{1}^{2} + b_{2}^{2} + \ldots + b_{n}^{2} \right) \geq \left( a_{1}b_{1} + \ldots + a_{n}b_{n} \right)^{2}\]

令
\(\mathbf{a} = \left( a_{1},a_{2},\ldots,a_{n} \right),\mathbf{b} = \left( b_{1},b_{2},\ldots,b_{n} \right)\)

\[\mathbf{a}^{2}\mathbf{b}^{2} \geq \left( \mathbf{a}\mathbf{b} \right)^{2}\]

            """
        ).to_edge(UP)

        t4 = MathTex(
            r"|a|^{2}|b|^{2} \geq \left( a b \right)^{2}",
        )
        t4[0][1].set_color(RED)
        t4[0][10].set_color(RED)
        t4[0][5].set_color(BLUE)
        t4[0][11].set_color(BLUE)

        self.play(Write(t3))
        self.wait()

        self.play(Transform(t3, t4))
        self.wait()

        self.play(t3.animate.to_corner(UL))

        npl = self.add_axes(animate=True)

        [ax, ay] = [ValueTracker(1), ValueTracker(2)]
        [bx, by] = [ValueTracker(-1), ValueTracker(2)]

        vec_a = always_redraw(
            lambda: Vector([ax.get_value(), ay.get_value()], color=RED)
        )
        vec_b = always_redraw(
            lambda: Vector([bx.get_value(), by.get_value()], color=BLUE)
        )
        factor = lambda: (
            np.dot(
                [ax.get_value(), ay.get_value()],
                [bx.get_value(), by.get_value()],
            )
            / (
                np.dot(
                    [ax.get_value(), ay.get_value()],
                    [ax.get_value(), ay.get_value()],
                )
                or 1
            )
        )
        vec_p = always_redraw(
            lambda: Vector(
                [
                    ax.get_value() * (factor() or 0.0001),
                    ay.get_value() * (factor() or 0.0001),
                ],
                color=GREEN,
            )
        )
        line_p = always_redraw(
            lambda: DashedLine(vec_p.get_end(), vec_b.get_end(), color=GREEN)
        )

        self.play(GrowArrow(vec_a), GrowArrow(vec_b), Create(vec_p), Create(line_p))
        l_a = self.label_vector(vec_a, "a", animate=False)
        l_a.add_updater(lambda s: s.move_to(vec_a.get_midpoint() + LEFT * 0.2))
        l_b = self.label_vector(vec_b, "b", animate=False)
        l_b.add_updater(lambda s: s.move_to(vec_b.get_midpoint() + LEFT * 0.2))
        l_p = self.label_vector(vec_p, "p", animate=False)
        l_p.add_updater(lambda s: s.move_to(vec_p.get_midpoint() + RIGHT * 0.2))

        t5 = MathTex(
            r"|a|^{2}|b|^{2} \geq \left( a b \right)^{2} = (|a| |p|)^{2}",
        )
        t5[0][1].set_color(RED)
        t5[0][10].set_color(RED)
        t5[0][5].set_color(BLUE)
        t5[0][11].set_color(BLUE)
        t5[0][17].set_color(RED)
        t5[0][20].set_color(GREEN)
        t5.next_to(t3, DOWN).align_to(t3, LEFT)

        self.play(Write(t5))

        self.play(ax.animate.set_value(3), ay.animate.set_value(4), run_time=2)
        self.play(ax.animate.set_value(3), ay.animate.set_value(-4), run_time=2)
        self.play(ax.animate.set_value(-1), ay.animate.set_value(-2), run_time=2)
        self.play(ax.animate.set_value(1), ay.animate.set_value(-2), run_time=2)
        self.play(ax.animate.set_value(2), ay.animate.set_value(-4), run_time=2)
        self.play(ax.animate.set_value(-1.5), ay.animate.set_value(3), run_time=2)

        self.wait()


class TestTex(Scene):
    def construct(self):
        t = MathTex(
            r"|a|^{2}|b|^{2} \geq \left( a b \right)^{2} = (|a| |c|)^{2}",
        )
        self.add(index_labels(t[0]), t)


class QED(Scene):
    def construct(self):
        self.play(Write(Tex("Q.E.D.")), run_time=3)
