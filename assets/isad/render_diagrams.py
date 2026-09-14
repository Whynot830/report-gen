"""Схемы логической и физической архитектуры для ПР2."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parent


def _box(ax, x, y, w, h, text, *, fc="#4A90D9", ec="#1F4E79", tc="white", fs=8.5, lw=1.2, radius=0.08, weight="bold"):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3,
    )
    ax.add_patch(p)
    ax.text(
        x + w / 2, y + h / 2, text, ha="center", va="center",
        fontsize=fs, color=tc, zorder=4, fontweight=weight,
        linespacing=1.25, wrap=False,
    )
    return (x, y, w, h)


def _frame(ax, x, y, w, h, title, *, fc="#F4F7FB", ec="#7A8A9A", ls="--"):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=fc, edgecolor=ec, linewidth=1.1, linestyle=ls, zorder=1,
    )
    ax.add_patch(p)
    ax.text(x + 0.15, y + h - 0.22, title, ha="left", va="top", fontsize=8.2, color="#334155", fontweight="bold", zorder=2)


def _arrow(ax, x1, y1, x2, y2, label="", *, color="#334155"):
    ax.add_patch(
        FancyArrowPatch(
            (float(x1), float(y1)), (float(x2), float(y2)),
            arrowstyle="-|>", mutation_scale=11, linewidth=1.05,
            color=color, zorder=5, shrinkA=1, shrinkB=1,
        )
    )
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.12, label, ha="center", va="bottom", fontsize=6.4, color="#475569", zorder=6)


def _link(ax, a, sa, b, sb, label=""):
    x1, y1 = _mid(a, sa)
    x2, y2 = _mid(b, sb)
    _arrow(ax, x1, y1, x2, y2, label)


def _mid(box, side):
    x, y, w, h = box
    if side == "n":
        return x + w / 2, y + h
    if side == "s":
        return x + w / 2, y
    if side == "e":
        return x + w, y + h / 2
    if side == "w":
        return x, y + h / 2
    raise ValueError(side)


def render_logical():
    fig, ax = plt.subplots(figsize=(16.8, 10.4), dpi=180)
    ax.set_xlim(0, 17.2)
    ax.set_ylim(0, 10.6)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    actor = "#163A5F"
    ui = "#2563A8"
    app = "#3B82C4"
    data = "#0F766E"
    ext = "#6B7280"
    product = "#B45309"

    _box(ax, 0.25, 8.55, 2.5, 1.35, "Разработчик /\nаналитик\nпроектирует модель", fc=actor, fs=8)
    _box(ax, 0.25, 0.35, 2.5, 1.35, "DevOps-инженер\nзапускает генерацию\nв CI/CD", fc=actor, fs=8)

    _frame(ax, 3.05, 1.85, 10.55, 8.35, "ИС: Low-code платформа генерации инструментов администрирования")

    _frame(ax, 3.25, 8.35, 10.15, 1.55, "Уровень представления", fc="#E8F1FB", ec="#5B7C99", ls="-")
    editor = _box(ax, 5.55, 8.5, 5.55, 1.15, "Веб-редактор модели данных\nсущности, поля, связи 1:1 / 1:N / M:N", fc=ui, fs=8.2)

    _frame(ax, 3.25, 4.55, 10.15, 3.6, "Уровень приложений", fc="#EEF6FC", ec="#5B7C99", ls="-")
    dsl = _box(ax, 5.55, 6.7, 5.55, 1.1, "Модуль метамодели и DSL\nсериализация, валидация, diff версий", fc=app, fs=8.2)
    g_sql = _box(ax, 3.45, 4.75, 2.35, 1.45, "Генератор\nSQL-миграций", fc=app, fs=8)
    g_be = _box(ax, 5.95, 4.75, 2.35, 1.45, "Генератор\nbackend", fc=app, fs=8)
    g_ui = _box(ax, 8.45, 4.75, 2.35, 1.45, "Генератор\nадмин-панели", fc=app, fs=8)
    g_doc = _box(ax, 10.85, 6.7, 2.3, 1.1, "Генератор\nOpenAPI", fc=app, fs=7.8)
    g_rbac = _box(ax, 10.85, 4.75, 2.3, 1.45, "Генератор\nRBAC", fc=app, fs=8)

    _frame(ax, 3.25, 2.05, 10.15, 2.25, "Уровень данных и экспорта", fc="#ECF8F6", ec="#5B7C99", ls="-")
    cli = _box(ax, 3.45, 2.25, 4.7, 1.55, "Модуль импорта / экспорта и CLI\nсборка отчуждаемого репозитория", fc=data, fs=8)
    store = _box(ax, 8.45, 2.25, 4.7, 1.55, "Хранилище модели (текстовый DSL)\nверсионируемые JSON-документы", fc=data, fs=8)

    git = _box(ax, 14.05, 8.5, 2.85, 1.15, "Git / CI-CD\nвнешняя система", fc="#CA8A04", ec="#854D0E", fs=8)
    app_out = _box(ax, 14.05, 4.75, 2.85, 1.7, "Сгенерированное\nприложение\n(продукт вне платформы)", fc=product, ec="#7C2D12", fs=8)
    pg = _box(ax, 14.05, 2.25, 2.85, 1.55, "СУБД PostgreSQL\nданные целевого\nприложения", fc=ext, fs=8)

    _arrow(ax, 2.75, 9.25, *_mid(editor, "w"), label="HTTPS")
    a, b = _mid(editor, "s"); c, d = _mid(dsl, "n")
    _arrow(ax, a, b, c, d, "граф модели")
    a, b = _mid(dsl, "s")
    _arrow(ax, a, b, *_mid(g_be, "n"), label="DSL")
    a, b = _mid(dsl, "w"); c, d = _mid(g_sql, "n")
    _arrow(ax, a, b - 0.05, g_sql[0] + g_sql[2] / 2, g_sql[1] + g_sql[3], "")
    a, b = _mid(dsl, "e"); c, d = _mid(g_doc, "w")
    _arrow(ax, a, b, c, d, "")
    a, b = _mid(dsl, "s")
    _arrow(ax, dsl[0] + dsl[2] - 0.4, b, *_mid(g_ui, "n"), "")
    _arrow(ax, dsl[0] + dsl[2] + 0.15, dsl[1], *_mid(g_rbac, "n"), "")
    for g in (g_sql, g_be, g_ui, g_rbac):
        _arrow(ax, *_mid(g, "s"), g[0] + g[2] / 2, cli[1] + cli[3], "")
    _arrow(ax, *_mid(g_doc, "s"), cli[0] + cli[2] - 0.3, cli[1] + cli[3], "")
    a, b = _mid(dsl, "s"); _arrow(ax, dsl[0] + 1.1, dsl[1], *_mid(store, "n"), "версия DSL")
    _arrow(ax, *_mid(cli, "e"), *_mid(store, "w"), "")
    gx, gy = _mid(git, "s")
    _arrow(ax, store[0] + store[2], store[1] + store[3] / 2 + 1.4, gx, gy, "commit")
    _arrow(ax, *_mid(cli, "e"), *_mid(app_out, "w"), "артефакты")
    _arrow(ax, *_mid(app_out, "s"), *_mid(pg, "n"), "CRUD / миграции")
    _arrow(ax, 2.75, 1.05, *_mid(cli, "w"), label="CLI")

    ax.text(8.55, 0.22, "Сплошные стрелки — потоки модели, DSL и порождаемых артефактов. Пунктирная граница — контур информационной системы.", ha="center", fontsize=7.2, color="#64748B")
    fig.tight_layout(pad=0.25)
    path = OUT / "logical_architecture.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def render_physical():
    fig, ax = plt.subplots(figsize=(16.8, 11.0), dpi=180)
    ax.set_xlim(0, 17.4)
    ax.set_ylim(0, 11.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    actor = "#163A5F"
    edge = "#1D4E89"
    app = "#2563A8"
    data = "#0F766E"
    ext = "#6B7280"
    ops = "#7C3AED"
    warn = "#B45309"

    _box(ax, 0.2, 9.35, 2.35, 1.25, "Разработчик\nбраузер", fc=actor, fs=8)
    _box(ax, 0.2, 6.55, 2.35, 1.25, "CI-раннер\nGitHub Actions /\nGitLab CI", fc=actor, fs=7.8)

    _frame(ax, 2.75, 3.35, 10.85, 7.55, "Облако / VPC (контур безопасности)", fc="#F8FAFC", ec="#64748B", ls="-")
    _frame(ax, 2.95, 8.85, 4.55, 1.8, "Зона Edge / DMZ", fc="#E0E7FF", ec="#4338CA", ls="-")
    cdn = _box(ax, 3.15, 9.05, 2.0, 1.3, "CDN\nстатика SPA", fc=edge, fs=8)
    waf = _box(ax, 5.3, 9.05, 2.0, 1.3, "WAF + LB\nIngress", fc=edge, fs=8)

    _frame(ax, 2.95, 5.15, 10.45, 3.5, "Подсеть приложений · Kubernetes-кластер", fc="#E8F1FB", ec="#1D4E89", ls="-")
    ed = _box(ax, 3.15, 6.85, 3.15, 1.4, "Поды редактора\nNginx + React SPA", fc=app, fs=8)
    plat_api = _box(ax, 6.5, 6.85, 3.3, 1.4, "API платформы\nгенерация, валидация DSL", fc=app, fs=8)
    wrk = _box(ax, 10.0, 6.85, 3.15, 1.4, "Worker генерации\nAST / ts-morph", fc=app, fs=8)
    exporter = _box(ax, 3.15, 5.35, 4.7, 1.2, "CLI / job экспорта артефактов", fc=app, fs=8)
    cache = _box(ax, 8.05, 5.35, 5.1, 1.2, "Кэш заданий Redis (очередь генерации)", fc=app, fs=8)

    _frame(ax, 2.95, 3.55, 10.45, 1.4, "Подсеть данных", fc="#ECFDF5", ec="#0F766E", ls="-")
    rds = _box(ax, 3.15, 3.7, 4.7, 1.0, "Управляемый PostgreSQL\n(учётные записи, проекты)", fc=data, fs=8)
    s3 = _box(ax, 8.05, 3.7, 5.1, 1.0, "Объектное хранилище\nартефакты и бэкапы DSL", fc=data, fs=8)

    _frame(ax, 13.85, 5.15, 3.3, 5.45, "Внешние системы", fc="#FFF7ED", ec="#9A3412", ls="-")
    git = _box(ax, 14.05, 8.85, 2.9, 1.4, "Git-хостинг\nмодель + код", fc=warn, ec="#7C2D12", fs=8)
    gen = _box(ax, 14.05, 6.95, 2.9, 1.55, "Сгенерированное\nприложение\n(отдельный контур)", fc=warn, ec="#7C2D12", fs=8)
    tpg = _box(ax, 14.05, 5.35, 2.9, 1.3, "PostgreSQL\nцелевого проекта", fc=ext, fs=8)

    _frame(ax, 2.75, 0.25, 14.4, 2.85, "Сервисы эксплуатации (вне VPC или SaaS)", fc="#F5F3FF", ec="#6D28D9", ls="-")
    _box(ax, 2.95, 0.45, 3.3, 2.0, "Мониторинг\nPrometheus / Grafana\nалерты", fc=ops, fs=8)
    _box(ax, 6.45, 0.45, 3.4, 2.0, "Логирование\nцентрализованные логи\nи аудит генерации", fc=ops, fs=8)
    _box(ax, 10.05, 0.45, 3.4, 2.0, "Резервное копирование\nснимки БД и DSL\nв объектное хранилище", fc=ops, fs=8)
    _box(ax, 13.65, 0.45, 3.25, 2.0, "Секреты / IAM\nдоступ к Git и БД\nпо ролям", fc=ops, fs=8)

    _arrow(ax, 2.55, 10.0, *_mid(cdn, "w"), "HTTPS")
    _link(ax, cdn, "e", waf, "w")
    _link(ax, waf, "s", ed, "n", "статика")
    _arrow(ax, waf[0] + waf[2] / 2 + 0.4, waf[1], *_mid(plat_api, "n"), "API")
    _link(ax, ed, "e", plat_api, "w")
    _link(ax, plat_api, "e", wrk, "w", "job")
    ax1, ay1 = _mid(plat_api, "s")
    _arrow(ax, ax1 - 0.8, ay1, *_mid(exporter, "n"))
    _arrow(ax, ax1 + 1.4, ay1, *_mid(cache, "n"))
    _link(ax, exporter, "s", rds, "n")
    _link(ax, cache, "s", s3, "n")
    _arrow(ax, 2.55, 7.15, *_mid(exporter, "w"), "CLI")
    _link(ax, wrk, "e", git, "w", "push")
    _link(ax, exporter, "e", gen, "w", "экспорт")
    _link(ax, gen, "s", tpg, "n", "миграции")
    sx, sy = _mid(s3, "s")
    _arrow(ax, sx, sy, 11.75, 2.45, "бэкап")

    ax.text(8.7, 3.15, "Сегментация: публичный периметр → кластер приложений → изолированная подсеть данных. Сгенерированное приложение живёт вне платформы.", ha="center", fontsize=7.1, color="#64748B")
    fig.tight_layout(pad=0.25)
    path = OUT / "physical_architecture.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def render_editor_wireframe():
    fig, ax = plt.subplots(figsize=(14.5, 8.6), dpi=170)
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 8.6)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.add_patch(Rectangle((0.2, 0.25), 14.1, 8.1, facecolor="#F8FAFC", edgecolor="#334155", lw=1.4))
    ax.add_patch(Rectangle((0.2, 7.55), 14.1, 0.8, facecolor="#163A5F", edgecolor="#163A5F"))
    ax.text(0.45, 7.95, "Low-code платформа  ·  Редактор модели данных", color="white", fontsize=11, va="center", fontweight="bold")
    ax.text(13.95, 7.95, "Проект: orders-mvp   Пользователь: аналитик", color="#DBEAFE", fontsize=8, va="center", ha="right")

    ax.add_patch(Rectangle((0.2, 0.25), 2.7, 7.3, facecolor="#EEF2FF", edgecolor="#94A3B8", lw=0.8))
    ax.text(1.55, 7.2, "Палитра", ha="center", fontsize=9, fontweight="bold", color="#1E3A5F")
    for i, name in enumerate(["Сущность", "Поле", "Связь 1:N", "Связь M:N", "Индекс"]):
        ax.add_patch(FancyBboxPatch((0.4, 6.35 - i * 0.7), 2.3, 0.55, boxstyle="round,pad=0.02,rounding_size=0.08", facecolor="white", edgecolor="#64748B"))
        ax.text(1.55, 6.62 - i * 0.7, name, ha="center", va="center", fontsize=8)

    ax.add_patch(Rectangle((2.9, 0.25), 8.3, 7.3, facecolor="#FFFFFF", edgecolor="#94A3B8", lw=0.8))
    ax.text(7.05, 7.2, "Холст модели", ha="center", fontsize=9, fontweight="bold", color="#1E3A5F")

    def entity(x, y, title, fields):
        h = 0.42 + 0.32 * len(fields)
        ax.add_patch(FancyBboxPatch((x, y), 2.45, h, boxstyle="round,pad=0.02,rounding_size=0.06", facecolor="#DBEAFE", edgecolor="#1D4E89", lw=1.1))
        ax.add_patch(Rectangle((x, y + h - 0.42), 2.45, 0.42, facecolor="#1D4E89"))
        ax.text(x + 1.225, y + h - 0.21, title, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        for i, f in enumerate(fields):
            ax.text(x + 0.12, y + h - 0.62 - i * 0.32, f, fontsize=7.2, color="#0F172A", va="center")
        return x + 2.45, y + h / 2

    e1 = entity(3.3, 4.35, "Order", ["id : uuid", "status : enum", "total : money"])
    e2 = entity(6.55, 4.55, "OrderItem", ["id : uuid", "qty : int", "price : money"])
    e3 = entity(3.3, 1.35, "Customer", ["id : uuid", "email : string"])
    e4 = entity(6.7, 1.55, "Product", ["id : uuid", "sku : string"])
    ax.annotate("", xy=(6.55, 5.55), xytext=(5.75, 5.55), arrowprops=dict(arrowstyle="-|>", color="#334155"))
    ax.text(6.15, 5.7, "1:N", fontsize=7, ha="center")
    ax.annotate("", xy=(4.5, 4.35), xytext=(4.5, 3.05), arrowprops=dict(arrowstyle="-|>", color="#334155"))
    ax.text(4.75, 3.7, "N:1", fontsize=7)
    ax.annotate("", xy=(6.7, 2.7), xytext=(8.95, 4.55), arrowprops=dict(arrowstyle="-|>", color="#334155"))

    ax.add_patch(Rectangle((11.2, 0.25), 3.1, 7.3, facecolor="#F1F5F9", edgecolor="#94A3B8", lw=0.8))
    ax.text(12.75, 7.2, "Свойства / генерация", ha="center", fontsize=8.5, fontweight="bold", color="#1E3A5F")
    ax.text(11.4, 6.7, "Сущность: Order", fontsize=8)
    ax.text(11.4, 6.3, "Поля: 3   Связи: 2", fontsize=8)
    ax.add_patch(FancyBboxPatch((11.4, 5.35), 2.7, 0.7, boxstyle="round,pad=0.02,rounding_size=0.08", facecolor="#0F766E", edgecolor="#0F766E"))
    ax.text(12.75, 5.7, "Сгенерировать", ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
    ax.text(11.4, 4.9, "Артефакты:", fontsize=8, fontweight="bold")
    for i, t in enumerate(["Prisma / SQL", "NestJS CRUD", "Admin UI", "OpenAPI", "RBAC"]):
        ax.text(11.5, 4.5 - i * 0.4, f"☑  {t}", fontsize=8, color="#334155")
    ax.text(11.4, 2.2, "Валидация DSL: OK", fontsize=8, color="#0F766E")
    ax.text(11.4, 1.7, "Анти-drift: merge", fontsize=8, color="#334155")
    ax.text(11.4, 1.15, "Экспорт репозитория", fontsize=8, color="#1D4E89")

    fig.tight_layout(pad=0.2)
    path = OUT / "editor_wireframe.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


if __name__ == "__main__":
    for fn in (render_logical, render_physical, render_editor_wireframe):
        p = fn()
        print(p)
