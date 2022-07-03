


def change_temperature(chunks, temp: int):
    if temp >= 16 and temp <= 30:
        if temp >= 21:
            
            chunks[27] = "10"
        chunks[14] = bin(temp * 8).replace("0b", "")[::-1]
    else:
        print("Invalid temperature setting to default temperature [16]")
        chunks[14] = bin(16*8).replace("0b", "")[::-1]
    log_file = open("/home/renessmey/apps/astroboy/app.log", "a+")
    log_file.write(f"\n chunks : {chunks}")
    return chunks
def turn_ac_on(chunks):
    chunks[13] = "00100011"
    return chunks

def turn_ac_off(chunks):
    chunks[13] = "00000011"
    return chunks

def perform_checksum(chunks):
    if chunks:
        last_byte=0b0
        for i in range(9,26):
            #print(chunks[i])
            last_byte = last_byte + int("0b"+chunks[i][::-1], 2)
        chunks[26] =bin(last_byte & 0xFE)
        chunks[26] = format(int(chunks[26], 2), 'b').zfill(8)[::-1]
        print(chunks)
        return chunks



    
