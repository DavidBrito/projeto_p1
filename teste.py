poligono = [[(42.252649, -79.76278), (42.000709, -79.76278), (42.000709, -75.35932), (41.863786, -75.249781), (41.869263, -75.173104), (41.754247, -75.052611), (41.60637, -75.074519), (41.436584, -74.89378), (41.431108, -74.740426), (41.359907, -74.69661), (41.288707, -74.828057), (41.179168, -74.882826), (40.971045, -75.134765), (40.866983, -75.052611), (40.691721, -75.205966), (40.576705, -75.195012), (40.543843, -75.069042), (40.417874, -75.058088), (40.215227, -74.773287), (40.127596, -74.82258), (39.963288, -75.129289), (39.88661, -75.145719), (39.804456, -75.414089), (39.831841, -75.616736), (39.722302, -75.786521), (39.722302, -79.477979), (39.722302, -80.518598), (40.636951, -80.518598), (41.978802, -80.518598), (41.978802, -80.518598), (42.033571, -80.332382), (42.269079, -79.76278), (42.252649, -79.76278)]]

polygon = poligono[0]

numero_vertices = len(polygon)
area = 0
x = 0
y = 1
somatorio = 0

# area

for i in range(0, numero_vertices - 1):
    somatorio += (polygon[i][x] * polygon[i + 1][y]) - \
            (polygon[i + 1][x] * polygon[i][y])

area = abs(somatorio / 2)

somatorio = 0
# centroid_x

for i in range(0, numero_vertices - 1):
    somatorio += (polygon[i][x] + polygon[i+1][x]) * \
      (polygon[i][x] * polygon[i+1][y] - polygon[i+1][x] * polygon[i][y])

centroid_x = somatorio / (6 * area)
somatorio = 0
# centroid_y

for j in range(0, numero_vertices - 1):
    somatorio += (polygon[j][y] + polygon[j+1][y]) * \
      (polygon[j][x] * polygon[j+1][y] - polygon[j+1][x] * polygon[j][y])

centroid_y = somatorio / (6 * area)


print(area)
print(centroid_x)
print(centroid_y)
