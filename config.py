import folium

__name__ = "SIPLA"

__subname__ = "Sistema Integrado de Planejamento"

__version__ = "0.0.1 (ALPHA)"

sipla_icon = "img/logo.png"

sipla_stylesheet = "fusion"


##colorsList = QColor.colorNames()
colorsList = ['black', 'blue', 'blueviolet', 'brown', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', \
              'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', \
              'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darksalmon', 'darkseagreen', 'darkslateblue',\
              'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', \
              'dimgrey', 'dodgerblue', 'firebrick', 'forestgreen', 'fuchsia', 'gold', 'goldenrod', 'gray', 'green', \
              'greenyellow', 'grey', 'hotpink', 'indigo', 'lime', 'limegreen', 'magenta', 'maroon', 'mediumaquamarine', \
              'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumturquoise', \
              'midnightblue', 'navy', 'olive', 'olivedrab', 'orange', 'orchid', 'peru', 'plum', 'powderblue', 'purple', \
              'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'sienna', 'silver', 'skyblue', \
              'slateblue', 'slategray', 'slategrey', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', \
              'turquoise', 'violet', 'yellowgreen']

# Add custom basemaps to folium
basemaps = {
    'Google Maps': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Maps',
        overlay=True,
        control=True
    ),
    'Google Satellite': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        overlay=True,
        control=True
    ),
    'Google Terrain': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Terrain',
        overlay=True,
        control=True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        overlay=True,
        control=True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=True,
        control=True
    )
}
