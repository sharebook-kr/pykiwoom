import zipfile

DIR_PATH = "C:/OpenAPI/data/"

def read_enc(opt_fname):
    fpath = DIR_PATH + "{}.enc".format(opt_fname)
    enc = zipfile.ZipFile(fpath)
    dat_name = opt_fname.upper() + ".dat"
    lines = enc.read(dat_name).decode("cp949")
    return lines

def parse_block(data):
    block_info = data[0]
    block_type = None
    if 'INPUT' in block_info:
        block_type = 'input'
    else:
        block_type = 'output'

    record_line = data[1]
    tokens = record_line.split('_')[1].strip()
    record = tokens.split("=")[0]

    fields = data[2:-1]
    field_name = []
    for line in fields:
        field = line.split("=")[0].strip()
        field_name.append(field)

    ret_data = {}
    ret_data[record] = field_name
    return block_type, ret_data


def parse_dat(trcode, lines):
    lines = lines.split('\n')
    start_indices = [i for i, x in enumerate(lines) if x.startswith("@START")]
    end_indices = [i for i, x in enumerate(lines) if x.startswith("@END")]

    block_indices = zip(start_indices, end_indices)

    enc_data = {"trcode": trcode, "input": [], "output": []}

    for start, end in block_indices:
        block_data = lines[start-1:end+1]
        block_type, fields = parse_block(block_data)
        if block_type == "input":
            enc_data["input"].append(fields)
        else:
            enc_data["output"].append(fields)

    return enc_data


if __name__ == "__main__":
    import pprint

    #lines = read_enc("opt10001")
    #data = parse_dat("opt10001", lines)
    #pprint.pprint(data)

    lines = read_enc("opt10081")
    data = parse_dat("opt10081", lines)
    pprint.pprint(data)
