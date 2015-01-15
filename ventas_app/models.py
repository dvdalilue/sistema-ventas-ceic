from django.db import models
from django.db.models  import *
#from django.conf import settings
from datetime import datetime

class Usuario(models.Model):
    """Usuario que usa el sistema"""
    TIPOS    = (
        ('A', 'Administrador'),
        ('U', 'Usuario'      ),
        ('C', 'Cliente'      ),
        )
    cedula   = models.IntegerField(max_length=8, primary_key = True)
    carnet   = models.CharField(max_length=8, unique = True)
    nombre   = models.CharField(max_length=32)
    fecha    = models.DateTimeField('fecha de inscripcion')
    tipo     = models.CharField(max_length=1, choices=TIPOS)
    saldo    = models.DecimalField(max_digits=9, decimal_places=2)
    
    def saldo_str(self): return str(self.saldo).rstrip('0').rstrip('.')
    saldo_str.short_description = 'Saldo'
    
    def aporte(self):
        movs = MovimientoVentas.objects.filter(factura__usuario = self).exclude(tipo='D').exclude(tipo='R').aggregate(r=Sum('cantidad'));
        return movs['r']
        
    def aporte_str(self): return str(self.aporte()).rstrip('0').rstrip('.')
    aporte_str.short_description = 'Aporte'
    
    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ['fecha']

class Producto(models.Model):
    """Productos a la venta"""
    nombre   = models.CharField(max_length=128, unique = True)
    cantidad = models.IntegerField()
    imagen   = models.ImageField(upload_to = "Imagenes/Productos/")
    ventas   = models.IntegerField(default = 0)
    descripcion = models.CharField(max_length=128, null = True)
    proveedor = models.CharField(max_length=128, null = True)
    
    def get_nombre(self):
        return self.nombre

    def get_descripcion(self):
        return self.descripcion

    def get_proveedor(self):
        return self.proveedor

    def precio_obj(self):
        precios = self.precio_set.filter(fecha__lte = datetime.now);
        if(precios.count() > 0):
            return precios[0]
        else:
            return None
    
    def precio(self):
        p = self.precio_obj()
        if(p != None):
            return p.valor
        else:
            return 0.0
        
    def precio_str(self):
        return str(self.precio()).rstrip('0').rstrip('.')
    precio_str.short_description = 'Precio'

    def imagen_tag(self):
        if self.imagen:
            return '<img src="%s" width="64px" height="64px" />' % (self.imagen.url)
        else:
            return '(Sin imagen)'
    imagen_tag.short_description = 'Imagen'
    imagen_tag.allow_tags = True
    
    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ['-ventas']

class Precio(models.Model):
    """Precio de un producto en un determinado momento"""
    producto = models.ForeignKey(Producto)
    valor    = models.DecimalField(max_digits=9, decimal_places=3)
    fecha    = models.DateTimeField('fecha de validez', unique = True)
    
    def __unicode__(self):
        return self.producto.nombre+" "+str(self.valor)+" Bfs" #self.fecha.strftime("%d-%m-%Y : %I %p")
    
    class Meta:
        ordering = ['-fecha']
    
class Factura(models.Model):
    """Representa un movimiento de caja y productos a un usuario en una fecha y tiene asociados ventas de productos y Movimientos de caja"""
    fecha    = models.DateTimeField('fecha de expedicion')
    usuario  = models.ForeignKey(Usuario, null = True)
    
    def total(self):
        return self.ventaproducto_set.aggregate(r=Sum('precio__valor'))['r']
    
    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ['-fecha']
    
    

class VentaProducto(models.Model):
    """Cantidad de productos vendidos en una factura"""
    producto = models.ForeignKey(Producto)
    factura  = models.ForeignKey(Factura)
    cantidad = models.IntegerField()
    precio   = models.ForeignKey(Precio)
    
    def __unicode__(self):
        return self.producto.nombre
    
    def usuario(self): return self.factura.usuario

    class Meta:
        unique_together = ('producto', 'factura',)

class Movimiento(models.Model):
    """Cantidad de dinero involucrado en un movimiento de caja"""
    cantidad = models.DecimalField(max_digits=9, decimal_places=3)
    
    def __unicode__(self):
        return "Mov "+str(self.id)
    
    class Meta:
        abstract = True;

class MovimientoVentas(Movimiento):
    """Cantidad de dinero involucrado en un movimiento de caja en una Factura"""
    TIPOS    = (
        ('E', 'Efectivo'),
        ('S', 'Saldo'   ),
        ('D', 'Donacion'),
        ('R', 'Recarga' ),
        )
    tipo     = models.CharField(max_length=1, choices = TIPOS)
    factura  = models.ForeignKey(Factura)
    
    class Meta:
        unique_together = ('factura', 'tipo')

class MovimientoCaja(Movimiento):
    """Cantidad de dinero involucrado en un movimiento de caja"""
    TIPOS    = (
        ('P', 'Ajuste Positivo'),
        ('N', 'Ajuste Negativo'),
        ('Z', 'Retiro'         ),
        ('I', 'Ingreso'        ),
        )
    tipo     = models.CharField(max_length=1, choices = TIPOS)
    descripcion = models.TextField()
    fecha = models.DateTimeField()

    def get_descripcion(self):
        return self.descripcion

    class Meta:
        ordering = ['-fecha']
"""
class CompraInventario(models.Model):
Compra de productos para aumentar el inventario
    producto = models.ForeignKey(Producto, unique_for_date = 'fecha')
    fecha    = models.DateTimeField('fecha de compra')
    cantidad = models.IntegerField()
    precio   = models.DecimalField(max_digits=6, decimal_places=2)
"""

class Turno(models.Model):
    cajero          = models.CharField(max_length=32)
    fecha_inicio    = models.DateTimeField('fecha de inicio', unique = True)
    fecha_fin       = models.DateTimeField('fecha de inicio', unique = True , null = True)
    ajuste          = models.ForeignKey(MovimientoCaja, null = True)

    class Meta:
        unique_together = ('fecha_inicio', 'cajero')
        ordering = ['-fecha_inicio']

class EfectivoReal(models.Model):
    """Cantidad de unidades de efectivo de cierta denominacion en caja"""
    DENOMINACION = (
        (0.01 , '0.01 Bfs' ),
        (0.05 , '0.05 Bfs' ),
        (0.1  , '0.1 Bfs'  ),
        (0.125, '0.125 Bsf'),
        (0.25 , '0.25 Bfs' ),
        (0.5  , '0.5 Bfs'  ),
        (1    , '1 Bfs'    ),
        (2    , '2 Bsf'    ),
        (5    , '5 Bsf'    ),
        (10   , '10 Bsf'   ),
        (20   , '20 Bsf'   ),
        (50   , '50 Bsf'   ),
        (100  , '100 Bsf'  ),
        )
    denominacion = models.DecimalField(max_digits=9, decimal_places=3, choices = DENOMINACION, primary_key = True) #Esto se debe cambiar si cambian los billetes
    imagen       = models.ImageField(upload_to="Imagenes/Efectivo/")
    
class CompraInventario(models.Model):
    """Representa la compra de inventario de un producto en especifico"""
    producto = models.ForeignKey(Producto)
    cantidad = models.IntegerField()
    fecha    = models.DateTimeField('fecha de compra', unique = True)
    costo    = models.DecimalField(max_digits=9, decimal_places=3, null=True)
    
    def __unicode__(self):
        return str(self.cantidad)+" "+str(self.producto)

class Efectivo(models.Model):
    """Cantidad de unidades de efectivo de cierta denominacion en caja"""
    MODIFICADO = (
        ('T', 'True'),
        ('F', 'False'),
    )
    modificado   = models.CharField(max_length=1, choices = MODIFICADO)
    cantidad     = models.IntegerField()
    denominacion = models.ForeignKey(EfectivoReal)
    turno_cajero = models.ForeignKey(Turno)

    class Meta:
        unique_together = ('turno_cajero', 'denominacion')
        ordering = ['turno_cajero']
