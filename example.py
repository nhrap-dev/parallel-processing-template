import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import psycopg2
import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import sys
from time import time

from credentials import host, username, password, database, port


class Workers:
    """Intializes a class of workers for parallel processing or thread pooling \n
    Keyword Arguments:
        func: method -- any method that takes a list as it's single argument
        iterables: list -- a list of arguments to be mapped to func
        asyncronous: Boolean -- when True runs the operation in parallel; when False runs the operation in thread pool
    """
    def __init__(self, func, iterables, asyncronous=True):
        t0 = time()
        if len(sys.argv) >= 3:
            cpus = int(sys.argv[2])
        else:
            cpus = os.cpu_count()
        workloadInterval = round(len(iterables) / cpus)
        location = 0
        workloads = []
        if asyncronous:
            with Pool() as executor: # async - fastest on large datasets
                for idx in range(cpus):
                    if idx < cpus - 1:
                        workload = iterables[location:location + workloadInterval]
                        location += workloadInterval
                    else:
                        workload = iterables[location:]
                    workloads.append(workload)
                executor.map(func, workloads)
        else:
            with ThreadPoolExecutor() as executor: # sequential - fastest on medium datasets
                for idx in range(cpus):
                    if idx < cpus - 1:
                        workload = iterables[location:location + workloadInterval]
                        location += workloadInterval
                    else:
                        workload = iterables[location:]
                    workloads.append(workload)
                executor.map(func, workloads)
        print('Total processing time: ' + str(time() - t0))


def work(iterables):
    """Generates a map thumbnail for every primary key in iterables"""
    conn = psycopg2.connect(host=host, user=username, password=password, dbname=database, port=port)
    cursor = conn.cursor()
    outputPath = './server/static/thumbnails/'
    for iterable in iterables:
        if not ".".join([str(iterable), 'png']) in os.listdir(outputPath):
            try:
                sql = 'select geom from api_geometry where id = ' + str(iterable)
                gdf = gpd.GeoDataFrame.from_postgis(sql, conn, geom_col='geom')
            except:
                cursor.execute("ROLLBACK")
                sql = 'select geom from api_geometry where id = ' + str(iterable)
                gdf = gpd.GeoDataFrame.from_postgis(sql, conn, geom_col='geom')
            gdf = gdf.to_crs('epsg:3857')
            ax = gdf.plot(figsize=(5, 5), alpha=0.5, edgecolor='k')
            provider = ctx.providers.OpenStreetMap.Mapnik
            provider['attribution'] = ''
            ax.set_axis_off()
            ax.axis('equal')
            plt.tight_layout()
            ctx.add_basemap(ax, url=ctx.providers.OpenStreetMap.Mapnik)
            plt.savefig(outputPath + str(iterable) + ".png", bbox_inches='tight', pad_inches=0, dpi=100)
            plt.close()


def baseline(func, iterables):
    """Runs work without parallel processing or thread pooling to get a baseline execution speed"""
    t0 = time()
    func(iterables)
    print('Baseline processing time: ' + str(time() - t0))
    

if __name__=='__main__':
    conn = psycopg2.connect(host=host, user=username, password=password, dbname=database, port=port)
    cursor = conn.cursor()
    cursor.execute('select id from api_geometry')
    outputPath = './server/static/thumbnails/'
    queryset = cursor.fetchall()
    iterables = [x[0] for x in queryset]
    if len(sys.argv) > 1 and sys.argv[1] == 'baseline':
        baseline(work, iterables)
    else:
        if sys.argv[1] == 'parallel':
            Workers(work, iterables, asyncronous=True)
        elif sys.argv[1] == 'thread':
            Workers(work, iterables, asyncronous=False)
        else:
            scriptname = os.path.basename(__file__)
            print("""ERROR: Unable to understand system argument.\nTry one of the following: \n  
                  python {s} parallel <workers:int> \n  
                  python {s} thread <workers:int> \n  
                  python {s} baseline
                """.format(s=scriptname))
