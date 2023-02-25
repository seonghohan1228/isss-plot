from datetime import datetime
from functions import find_data

MEPD_DT_A = 3
MEPD_DT_B = 4

class ISSSData:
    def set_data(self, data):
        hepd_data, mepd_data = data[0], data[1]
        # Convert UNIX time to datetime object
        hepd_time = [datetime.fromtimestamp(x) for x in find_data(hepd_data, 0, 'TIME_x')]
        mepd_time = [datetime.fromtimestamp(x) for x in find_data(mepd_data, 0, 'TIME')]
        # PC1 data
        hepd_pc1 = find_data(hepd_data, 0, 'PC1')
        mepd_pc1 = find_data(mepd_data, 0, 'PC1')
        mepd_dt = find_data(mepd_data, 0, 'DT')
        mepd_time_a, mepd_time_b, mepd_pc1_a, mepd_pc1_b = [], [], [], []
        # Find where DT in MEPD_SCI data changes to divide MEPD-A and MEPD-B
        for i in range(len(mepd_dt)):
            if mepd_dt[i] == MEPD_DT_A:
                mepd_time_a.append(mepd_time[i])
                mepd_pc1_a.append(mepd_pc1[i])
            elif mepd_dt[i] == MEPD_DT_B:
                mepd_time_b.append(mepd_time[i])
                mepd_pc1_b.append(mepd_pc1[i])
        self.time = [hepd_time, mepd_time_a, mepd_time_b]
        self.pc1 = [hepd_pc1, mepd_pc1_a, mepd_pc1_b]

        # Positional data ('LONG' 'LATT' data from HEPD file and MEPD file are identical) - pandas dataframe
        # HEIGHT data in meters. Converted to kilometers
        self.position = [find_data(hepd_data, 1, 'LONG'), find_data(hepd_data, 1, 'LATT'), find_data(hepd_data, 1, 'HEIGHT')/1000]

        # Magnetic data
        self.magnetic = []
        for i in range(4):
            self.magnetic.append(find_data(hepd_data, 1, f'TAMp_{i}'))
        for i in range(4):
            self.magnetic.append(find_data(hepd_data, 1, f'TAMr_{i}'))
