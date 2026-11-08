"""Zajedničke funkcije za čitanje ArcGIS File Geodatabase bez ArcGIS-a (EUPL-1.2)."""
import zlib, pathlib
import numpy as np, pyogrio
from rasterio.transform import from_origin


def table_ids(gdb):
    """Ime sloja -> datoteka aXXXXXXXX u .gdb mapi (iz GDB_SystemCatalog)."""
    gdb = pathlib.Path(gdb)
    cat = pyogrio.read_dataframe(gdb / "a00000001.gdbtable", read_geometry=False, fid_as_index=True)
    return {r.Name: f"a{fid:08x}" for fid, r in cat.iterrows()}


def read_raster(gdb, ids, name, dtype=">f4"):
    """Rasterska traka iz fras_bnd/fras_blk tablica (blokovi 128x128, zlib ili nekomprimirano, s bitmaskom)."""
    gdb = pathlib.Path(gdb)
    b = pyogrio.read_dataframe(gdb / f"{ids['fras_bnd_' + name]}.gdbtable", read_geometry=False).iloc[0]
    W, H, bw, bh = int(b.band_width), int(b.band_height), int(b.block_width), int(b.block_height)
    dt = np.dtype(dtype); n = bw * bh * dt.itemsize
    arr = np.full((-(-H // bh) * bh, -(-W // bw) * bw), np.nan, np.float32)
    blk = pyogrio.read_dataframe(gdb / f"{ids['fras_blk_' + name]}.gdbtable", read_geometry=False)
    blk = blk[blk.rrd_factor == 0]
    for r, c, d in zip(blk.row_nbr, blk.col_nbr, blk.block_data):
        if d is None: continue
        if d[:2] == b"\x78\x9c": d = zlib.decompress(d)
        v = np.frombuffer(d[:n], dt).reshape(bh, bw).astype(np.float32)
        if len(d) > n:
            m = np.unpackbits(np.frombuffer(d[n:n + bw * bh // 8], np.uint8)).reshape(bh, bw)
            v[m == 0] = np.nan
        arr[r * bh:(r + 1) * bh, c * bw:(c + 1) * bw] = v
    # eminx/emaxy su središta rubnih piksela
    cs = (b.emaxx - b.eminx) / (W - 1)
    return arr[:H, :W], from_origin(b.eminx - cs / 2, b.emaxy + cs / 2, cs, cs)
