# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "plotly",
#     "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _(mo):
    mo.md("## Vergleich: Gasheizung vs. PV / Solarthermie / Windkraft")

    energy_kwh = mo.ui.number(
        label="Energiebedarf / Energiemenge [kWh]",
        value=10000,
        step=100,
        start=0,
    )

    mo.md("### CO₂-Faktoren (g CO₂-eq/kWh) – anpassbar")

    c_gas = mo.ui.number(
        label="Gasheizung [g/kWh_th]",
        value=250,
        step=10,
        start=0,
    )
    c_pv = mo.ui.number(
        label="Photovoltaik (PV) [g/kWh_el]",
        value=50,
        step=5,
        start=0,
    )
    c_solarth = mo.ui.number(
        label="Solarthermie [g/kWh_th]",
        value=30,
        step=5,
        start=0,
    )
    c_wind = mo.ui.number(
        label="Windkraft [g/kWh_el]",
        value=15,
        step=5,
        start=0,
    )

    mo.md("### Kosten (€/kWh) – optionaler Kostenvergleich")

    price_gas = mo.ui.number(
        label="Gaspreis [€/kWh_th]",
        value=0.12,
        step=0.01,
        start=0,
    )
    price_pv = mo.ui.number(
        label="PV-Strom [€/kWh_el]",
        value=0.08,
        step=0.01,
        start=0,
    )
    price_solarth = mo.ui.number(
        label="Solarthermie-Wärme [€/kWh_th]",
        value=0.06,
        step=0.01,
        start=0,
    )
    price_wind = mo.ui.number(
        label="Windstrom [€/kWh_el]",
        value=0.07,
        step=0.01,
        start=0,
    )

    _layout = mo.vstack([
        mo.md("## Vergleich: Gasheizung vs. PV / Solarthermie / Windkraft"),
        energy_kwh,
        mo.md("### CO₂-Faktoren (g CO₂-eq/kWh) – anpassbar"),
        mo.hstack([c_gas, c_pv, c_solarth, c_wind], gap=1),
        mo.md("### Kosten (€/kWh) – optionaler Kostenvergleich"),
        mo.hstack([price_gas, price_pv, price_solarth, price_wind], gap=1),
    ])
    return (
        c_gas,
        c_pv,
        c_solarth,
        c_wind,
        energy_kwh,
        price_gas,
        price_pv,
        price_solarth,
        price_wind,
    )


@app.cell
def _(
    c_gas,
    c_pv,
    c_solarth,
    c_wind,
    energy_kwh,
    price_gas,
    price_pv,
    price_solarth,
    price_wind,
):
    # --- Hilfsfunktionen ---
    def total_co2_kg(g_per_kwh: float, energy: float) -> float:
        return (g_per_kwh * energy) / 1000

    def total_cost_eur(eur_per_kwh: float, energy: float) -> float:
        return eur_per_kwh * energy

    def fmt_de_int(x: float) -> str:
        return f"{x:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_de_money(x: float) -> str:
        return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_de_t(x: float) -> str:
        return fmt_de_money(x / 1000)

    # --- Berechnungen ---
    E = float(energy_kwh.value or 0)

    gas_kg = total_co2_kg(float(c_gas.value), E)
    pv_kg = total_co2_kg(float(c_pv.value), E)
    solarth_kg = total_co2_kg(float(c_solarth.value), E)
    wind_kg = total_co2_kg(float(c_wind.value), E)

    pv_save_kg = gas_kg - pv_kg
    solarth_save_kg = gas_kg - solarth_kg
    wind_save_kg = gas_kg - wind_kg

    gas_cost = total_cost_eur(float(price_gas.value), E)
    pv_cost = total_cost_eur(float(price_pv.value), E)
    solarth_cost = total_cost_eur(float(price_solarth.value), E)
    wind_cost = total_cost_eur(float(price_wind.value), E)

    pv_save_eur = gas_cost - pv_cost
    solarth_save_eur = gas_cost - solarth_cost
    wind_save_eur = gas_cost - wind_cost
    return (
        E,
        fmt_de_int,
        fmt_de_money,
        fmt_de_t,
        gas_cost,
        gas_kg,
        pv_cost,
        pv_kg,
        pv_save_eur,
        pv_save_kg,
        solarth_cost,
        solarth_kg,
        solarth_save_eur,
        solarth_save_kg,
        wind_cost,
        wind_kg,
        wind_save_eur,
        wind_save_kg,
    )


@app.cell
def _(
    c_gas,
    c_pv,
    c_solarth,
    c_wind,
    fmt_de_int,
    fmt_de_money,
    fmt_de_t,
    gas_cost,
    gas_kg,
    mo,
    pv_cost,
    pv_kg,
    pv_save_eur,
    pv_save_kg,
    solarth_cost,
    solarth_kg,
    solarth_save_eur,
    solarth_save_kg,
    wind_cost,
    wind_kg,
    wind_save_eur,
    wind_save_kg,
):
    rows = [
        ["Gasheizung (Referenz)", f"{float(c_gas.value):.0f}", fmt_de_int(gas_kg), "—", "—", fmt_de_money(gas_cost), "—"],
        ["Photovoltaik (PV)", f"{float(c_pv.value):.0f}", fmt_de_int(pv_kg), fmt_de_int(pv_save_kg), fmt_de_t(pv_save_kg), fmt_de_money(pv_cost), fmt_de_money(pv_save_eur)],
        ["Solarthermie", f"{float(c_solarth.value):.0f}", fmt_de_int(solarth_kg), fmt_de_int(solarth_save_kg), fmt_de_t(solarth_save_kg), fmt_de_money(solarth_cost), fmt_de_money(solarth_save_eur)],
        ["Windkraft", f"{float(c_wind.value):.0f}", fmt_de_int(wind_kg), fmt_de_int(wind_save_kg), fmt_de_t(wind_save_kg), fmt_de_money(wind_cost), fmt_de_money(wind_save_eur)],
    ]

    _table = mo.md(
        f"""
        <table style="width:100%; border-collapse:collapse; font-size:14px;">
          <thead>
            <tr style="text-align:left; border-bottom:1px solid #ddd;">
              <th style="padding:8px;">Technologie</th>
              <th style="padding:8px;">CO₂-Faktor [g/kWh]</th>
              <th style="padding:8px;">Gesamt-CO₂ [kg]</th>
              <th style="padding:8px;">Einsparung ggü. Gas [kg]</th>
              <th style="padding:8px;">Einsparung ggü. Gas [t]</th>
              <th style="padding:8px;">Kosten gesamt [€]</th>
              <th style="padding:8px;">Kosten-Vorteil ggü. Gas [€]</th>
            </tr>
          </thead>
          <tbody>
            {''.join([
              "<tr style='border-bottom:1px solid #eee;'>"
              f"<td style='padding:8px;'><b>{r[0]}</b></td>"
              f"<td style='padding:8px;'>{r[1]}</td>"
              f"<td style='padding:8px;'>{r[2]}</td>"
              f"<td style='padding:8px;'>{r[3]}</td>"
              f"<td style='padding:8px;'>{r[4]}</td>"
              f"<td style='padding:8px;'>{r[5]}</td>"
              f"<td style='padding:8px;'>{r[6]}</td>"
              "</tr>"
              for r in rows
            ])}
          </tbody>
        </table>
        """
    )

    _ergebnis = mo.vstack([
        mo.md("## Ergebnisse"),
        _table,
    ])
    return


@app.cell
def _(
    E,
    fmt_de_int,
    gas_cost,
    gas_kg,
    mo,
    plt,
    pv_cost,
    pv_kg,
    pv_save_eur,
    pv_save_kg,
    solarth_cost,
    solarth_kg,
    solarth_save_eur,
    solarth_save_kg,
    wind_cost,
    wind_kg,
    wind_save_eur,
    wind_save_kg,
):
    labels = ["Gas", "PV", "Solarthermie", "Wind"]
    co2_values = [gas_kg, pv_kg, solarth_kg, wind_kg]
    co2_savings = [0, pv_save_kg, solarth_save_kg, wind_save_kg]
    cost_values = [gas_cost, pv_cost, solarth_cost, wind_cost]
    cost_savings = [0, pv_save_eur, solarth_save_eur, wind_save_eur]

    fig1, ax1 = plt.subplots()
    ax1.bar(labels, co2_values)
    ax1.set_ylabel("Gesamt-CO₂ [kg]")
    ax1.set_title("Gesamt-CO₂ für E = " + fmt_de_int(E) + " kWh")

    fig2, ax2 = plt.subplots()
    ax2.bar(labels, co2_savings)
    ax2.axhline(0, color="black", linewidth=0.5)
    ax2.set_ylabel("Einsparung ggü. Gas [kg]")
    ax2.set_title("CO₂-Einsparung gegenüber Gas")

    fig3, ax3 = plt.subplots()
    ax3.bar(labels, cost_values)
    ax3.set_ylabel("Kosten gesamt [€]")
    ax3.set_title("Kosten für E = " + fmt_de_int(E) + " kWh")

    fig4, ax4 = plt.subplots()
    ax4.bar(labels, cost_savings)
    ax4.axhline(0, color="black", linewidth=0.5)
    ax4.set_ylabel("Kosten-Vorteil ggü. Gas [€]")
    ax4.set_title("Kosten-Vorteil gegenüber Gas")

    _diagramme = mo.vstack([
        mo.md("## Diagramme"),
        mo.hstack([fig1, fig2], gap=1),
        mo.hstack([fig3, fig4], gap=1),
    ])
    return


@app.cell
def _(mo):
    mo.md("""
    ## Formeln (Schul-/Klausurschreibweise)

    - Gesamt-CO₂ [kg] = (CO₂-Faktor [g/kWh] · E [kWh]) / 1000
    - Einsparung CO₂ [kg] = Gesamt-CO₂(Gas) − Gesamt-CO₂(Technologie)

    - Kosten [€] = Preis [€/kWh] · E [kWh]
    - Kosten-Vorteil [€] = Kosten(Gas) − Kosten(Technologie)

    Hinweis: PV/Wind liefern Strom, Solarthermie/Gas liefern Wärme.
    Für einen Schul-Prototyp ist der Vergleich über gleiche Energiemenge E in Ordnung.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt

    return mo, plt


if __name__ == "__main__":
    app.run()
