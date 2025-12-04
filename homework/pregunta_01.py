import pandas as pd
import matplotlib.pyplot as plt
import os


# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""


def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    def cargar_datos():
        tabla_envios = pd.read_csv("files/input/shipping-data.csv")
        return tabla_envios

    def grafico_envios_por_bodega(tabla):
        datos_local = tabla.copy()
        plt.figure()

        conteo = datos_local.Warehouse_block.value_counts()
        conteo.plot.bar(
            title="Shipping per Warehouse Block",
            xlabel="Warehouse Block",
            ylabel="Record Count",
            color="tab:blue",
            fontsize=8,
        )
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.savefig("docs/shipping_per_warehouse.png")

    def grafico_modo_envio(tabla):
        datos_local = tabla.copy()
        plt.figure()

        conteo = datos_local.Mode_of_Shipment.value_counts()
        conteo.plot.pie(
            title="Mode of Shipment",
            wedgeprops=dict(width=0.35),
            ylabel="",
            color=["tab:blue", "tab:orange", "tab:green"],
        )
        plt.savefig("docs/mode_of_shipment.png")

    def grafico_calificacion_promedio(tabla):
        datos_local = tabla.copy()
        plt.figure()

        resumen = (
            datos_local[["Mode_of_Shipment", "Customer_rating"]]
            .groupby("Mode_of_Shipment")
            .describe()
        )

        resumen.columns = resumen.columns.droplevel()
        resumen = resumen[["mean", "min", "max"]]

        plt.barh(
            y=resumen.index.values,
            width=resumen["max"].values - 1,
            left=resumen["min"].values,
            height=0.9,
            color="lightgrey",
            alpha=0.8,
        )

        lista_colores = [
            "tab:green" if valor >= 3.0 else "tab:orange"
            for valor in resumen["mean"].values
        ]

        plt.barh(
            y=resumen.index.values,
            width=resumen["mean"].values - 1,
            left=resumen["min"].values,
            color=lista_colores,
            height=0.5,
            alpha=1.0,
        )

        plt.title("Average Customer Rating by Mode of Shipment")
        plt.gca().spines["left"].set_color("grey")
        plt.gca().spines["bottom"].set_color("grey")
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        plt.savefig("docs/average_customer_rating.png")

    def grafico_distribucion_peso(tabla):
        datos_local = tabla.copy()
        plt.figure()

        datos_local.Weight_in_gms.plot.hist(
            title="Shipped Weight Distribution",
            color="tab:orange",
            edgecolor="white",
        )

        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.savefig("docs/weight_distribution.png")

    def generar_html():
        html = """<!DOCTYPE html>
        <html>
        <body>
            <h1>Shipping Dashboard Example</h1>
            <div style="width:45%;float:left">
            <img src="shipping_per_warehouse.png" alt="Fig 1">
            <img src="mode_of_shipment.png" alt="Fig 2">
            </div>
            <div style="width:45%;float:left">
            <img src="average_customer_rating.png" alt="Fig 3">
            <img src="weight_distribution.png" alt="Fig 4">
            </div>
        </body>
        </html>"""

        with open("docs/index.html", "w", encoding="utf-8") as fichero:
            fichero.write(html)

    # Ejecución del pipeline
    datos_cargados = cargar_datos()
    os.makedirs("docs", exist_ok=True)

    grafico_envios_por_bodega(datos_cargados)
    grafico_modo_envio(datos_cargados)
    grafico_calificacion_promedio(datos_cargados)
    grafico_distribucion_peso(datos_cargados)
    generar_html()


if __name__ == "__main__":
    pregunta_01()