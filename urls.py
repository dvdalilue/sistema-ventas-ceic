from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^sistemacaja/script$'      , 'ventas_app.views.script'),
    
    url(r'^sistemacaja/(?P<mensaje>\d*)$'      , 'ventas_app.views.index'),
    url(r'^sistemacaja/_login$'                , 'ventas_app.views.loguear'),
    url(r'^sistemacaja/_logout$'               , 'ventas_app.views.desloguear'),
    url(r'^sistemacaja/vender$'                , 'ventas_app.views.ver_vender'),
    url(r'^sistemacaja/comprar_do$'            , 'ventas_app.views.comprar'),
    url(r'^sistemacaja/compra_ok$'             , 'ventas_app.views.compra_ok'),
    url(r'^sistemacaja/inventario$'            , 'ventas_app.views.ver_inventario'),
    url(r'^sistemacaja/inventario/compra$'     , 'ventas_app.views.compra_inventario'),
	url(r'^sistemacaja/inventario/modificar$'  , 'ventas_app.views.modificar_inventario'),
    url(r'^sistemacaja/usuarios$'              , 'ventas_app.views.ver_usuarios'),
    url(r'^sistemacaja/caja$'                  , 'ventas_app.views.ver_caja_hoy'),
    url(r'^sistemacaja/caja/abrir$'            , 'ventas_app.views.ver_caja_abrir'),
    url(r'^sistemacaja/caja/cerrar$'           , 'ventas_app.views.ver_caja_cerrar'),
    url(r'^sistemacaja/movimientos$'           , 'ventas_app.views.ver_movimientos_hoy'),
    url(r'^sistemacaja/movimientos/fi=(?P<fi>\d{12})&ff=(?P<ff>\d{12})$'         
                                               , 'ventas_app.views.ver_movimientos'),
    url(r'^sistemacaja/caja/fi=(?P<fi>\d{12})&ff=(?P<ff>\d{12})$'
                                               , 'ventas_app.views.ver_caja'),
    
    url(r'^sistemacaja/listado_inventario_do$' , 'ventas_app.views.generar_lista_de_compras'),

    url(r'^sistemacaja/eliminar_usuario/(?P<id_cedula>[VE]\d{8})$', 'ventas_app.views.eliminar_usuario'),
    url(r'^sistemacaja/eliminar_producto/(?P<prod_id>\d+)$', 'ventas_app.views.eliminar_producto_inventario'),

    url(r'^sistemacaja/nuevo_usuario_do$'		 , 'ventas_app.views.nuevo_cliente'),
    url(r'^sistemacaja/nuevo_producto_do$'		 , 'ventas_app.views.nuevo_producto'),
    url(r'^sistemacaja/nuevo_movimiento_do$'	 , 'ventas_app.views.nuevo_movimiento'),
    url(r'^sistemacaja/inventario/compra_do$'	 , 'ventas_app.views.compra_inventario_do'),
	url(r'^sistemacaja/inventario/modificar_do$' , 'ventas_app.views.modificar_inventario_do'),
	url(r'^sistemacaja/caja/abrir_do$'		 	 , 'ventas_app.views.abrir_caja'),
	url(r'^sistemacaja/caja/cerrar_do$'		 	 , 'ventas_app.views.cerrar_caja'),

    url(r'^sistemacaja/ventas/ayuda$'      			 , 'ventas_app.views.ver_controlador_ayuda'),
    url(r'^sistemacaja/movimientos/ayuda$'			 , 'ventas_app.views.ver_controlador_ayuda'),
    url(r'^sistemacaja/usuarios/ayuda$'    			 , 'ventas_app.views.ver_controlador_ayuda'),
    url(r'^sistemacaja/inventario/ayuda$' 			 , 'ventas_app.views.ver_controlador_ayuda'),
    url(r'^sistemacaja/inventario/modificar/ayuda$'  , 'ventas_app.views.ver_controlador_ayuda'),
    url(r'^sistemacaja/inventario/compra/ayuda$'	 , 'ventas_app.views.ver_controlador_ayuda'),
    url(r'^sistemacaja/caja/ayuda$'   				 , 'ventas_app.views.ver_controlador_ayuda'),
    url(r'^sistemacaja/caja/abrir/ayuda$'   		 , 'ventas_app.views.ver_controlador_ayuda'),
    url(r'^sistemacaja/caja/cerrar/ayuda$'   		 , 'ventas_app.views.ver_controlador_ayuda'),
    
    url(r'^admin/', include(admin.site.urls)),

    #AJAX:
    url(r'^sistemacaja/buscar_productos$'   		 , 'ventas_app.views.buscar_productos'),
    url(r'^sistemacaja/buscar_usuario$'   		 , 'ventas_app.views.buscar_usuario'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        
        url(r'^templates/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.TEMPLATE_DIRS[0],
        }),
    )
