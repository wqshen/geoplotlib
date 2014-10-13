import sys,os
sys.path.append(os.path.realpath('..'))


from geoplotlib.layers import BaseLayer
from geoplotlib.core import BatchPainter
import geoplotlib
from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv


class TrailsLayer(BaseLayer):

    def __init__(self):
        self.data = read_csv('data/taxi.csv')
        self.data = self.data.where(self.data['taxi_id'] == list(set(self.data['taxi_id']))[2])
        self.t = self.data['timestamp'].min()
        self.painter = BatchPainter()

    def invalidate(self, proj):
        pass


    def draw(self, mouse_x, mouse_y, ui_manager):
        self.painter.batch_draw()
        ui_manager.info(epoch_to_str(self.t))


    def on_tick(self, dt, proj):
        self.painter = BatchPainter()
        self.painter.set_color([0,0,255])
        df = self.data.where((self.data['timestamp'] > self.t) & (self.data['timestamp'] <= self.t + 30*60))
        proj.fit(BoundingBox.from_points(lons=df['lon'], lats=df['lat']))
        x, y = proj.lonlat_to_screen(df['lon'], df['lat'])
        self.painter.points(x, y, 10)
        self.t += 5*60*dt


geoplotlib.add_layer(TrailsLayer())
geoplotlib.show()
