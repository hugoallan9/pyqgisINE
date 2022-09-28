'''
Ejemplo de uso del api de Qgis para python.
En este se carga un mapa departamental junto con un excel
para hacer un join, pintar el mapa coroplético y finalmente trabajar
el canvas para su exportación
'''
from pandas import read_excel
from qgis.core import (QgsVectorLayer,
                       QgsApplication,
                       QgsProject,
                       QgsFeature,
                       QgsField,
                       QgsVectorLayerJoinInfo
                       )

from PyQt5.QtCore import QVariant

#Creando el proyecto
QgsApplication.setPrefixPath("/usr", True)
qgs = QgsApplication([], True)
qgs.initQgis()
proyecto = QgsProject().instance()


#Carga del mapa
mapa = QgsVectorLayer("/home/hugog/GitHub/pyqgisExample/departamentos_gtm/departamentos_gtm.shp", "Mi mapa", "ogr")
idMapa = 0
print("No se pudo cargar el mapa de deptos")
proyecto.addMapLayer(mapa)
idMapa = mapa.id()
print(mapa.id())
# Imprimiendo la tabla de atributos
for feature in mapa.getFeatures():
    print(feature.attributes())


#Cargando el excel
datos = read_excel("/home/hugog/GitHub/pyqgisExample/datos_deptos.xlsx")
datos.fillna(0)

#Creando la capa de datos en el proyecto
temp = QgsVectorLayer("none", "result", "memory")
temp_data = temp.dataProvider()
# Inicio de la edición
temp.startEditing()

# Creación de los campos en el layer temporal
temp.addAttribute(QgsField("Cod_depto", QVariant.Double))
temp.addAttribute(QgsField("Protección", QVariant.Double))
# Actualización de los datos en el layer
temp.updateFields()

# Agregando los features
for row in datos.loc[:, ["Código Departamento", "Protección"]].itertuples():
    f = QgsFeature()
    f.setAttributes([row[1], row[2]])
    temp.addFeature(f)

# Empaquetando todo
temp.commitChanges()
# Agregar el layer al proyecto
idDatos = temp.id()
print(idDatos)
proyecto.instance().addMapLayer(temp)

#Hacer el join
info = QgsVectorLayerJoinInfo()
info.setJoinFieldName("Cod_depto")
info.setJoinLayerId(idDatos)
info.setJoinLayer(proyecto.instance().mapLayer(idDatos))
info.setTargetFieldName("departamen")
info.setPrefix("datos_")
proyecto.instance().mapLayer(idMapa).addJoin(info)
mapa.updateFields()
print('Los joins son', mapa.vectorJoins())

#Imprimiendo la tabla de atributos
for feature in mapa.getFeatures():
    print(feature.attributes())


