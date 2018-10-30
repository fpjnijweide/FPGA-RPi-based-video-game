# Input: decimal number
# Output: 8 bit binary representation of the input number
def digestDecimal(send_value):
    send_value_bin=bin(send_value)[2:]
    if len(send_value_bin) > 8:
        print("overflow")
        return -1
    if len(send_value_bin)<8:
        diff=8-len(send_value_bin)
        zerolist=diff*['0']
        zerostring=''.join(zerolist)
        send_value_bin=zerostring+send_value_bin
    return send_value_bin

# Input: binary representation of a minifloat
# Output: decimal value of the minifloat
def binToMinifloat(bin):
    if (len(bin) != 8):
        print("Binary sequence entered is not 8 bits long!")
        return "not 8 bits long"
    bin_string = ''.join(bin)
    sign = bin_string[0]
    exponent = bin_string[1:5]
    mantissa = bin_string[5:]
    if (exponent == "1111"):
        if (mantissa == "000"):
            print("Binary sequence entered represents infinity(NaN)")
            return "infinity"
        else:
            print("Binary sequence entered does not represent a number(NaN)")
            return "not a number"
    elif (bin_string == "00000000"):
        return float(0)
    else:
        sign_value = (-1)**int(sign)
        exponent_value = 2**(2 + int(exponent, 2))
        mantissa_value = float(1 + int(mantissa[0])*float(1/2) + int(mantissa[1])*float(1/4)
        + int(mantissa[2])*float(1/8))
        return sign_value*(mantissa_value*exponent_value)

# Input: Decimal value of a minifloat
# Output: Binary representation of the minifloat
def minifloatToBin(minifloat):
    res = ""
    minifloat = float(minifloat)
    if (minifloat > 0):
        sign = "0"
    elif (minifloat < 0):
        sign = "1"
    elif (minifloat == 0):
        return "00000000"
    exp = 0
    mantissa = ""
    minifloat = abs(minifloat)
    minifloat_int_bin = bin(int(minifloat))[2:]
    minifloat_fraction = minifloat - int(minifloat)
    minifloat_fraction_bin = ""
    for i in range(3):
        minifloat_fraction *= 2
        if (minifloat_fraction >= 1):
            minifloat_fraction_bin += "1"
            minifloat_fraction -= 1
        else:
            minifloat_fraction_bin += "0"
    mantissa = (minifloat_int_bin + minifloat_fraction_bin)[1:4]
    while minifloat > 1.0:
        exp += 1
        minifloat = float(minifloat)/10
    exponent = bin(exp)[2:]
    for i in range(4-len(exponent)):
        exponent = "0" + exponent
    res = sign + exponent + mantissa
    return res