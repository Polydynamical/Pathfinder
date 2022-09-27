import base64
import zlib
import numpy as np
import struct
import matplotlib.pyplot as plt


def parse(b64_string):
    # fix the 'inccorrect padding' error. The length of the string needs to be divisible by 4.
    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
    # convert the URL safe format to regular format.
    data = b64_string.replace("-", "+").replace("_", "/")

    data = base64.b64decode(data)  # decode the string
    data = zlib.decompress(data)  # decompress the data
    return np.array([d for d in data])


def parseHeader(depthMap):
    return {
        "headerSize": depthMap[0],
        "numberOfPlanes": getUInt16(depthMap, 1),
        "width": getUInt16(depthMap, 3),
        "height": getUInt16(depthMap, 5),
        "offset": getUInt16(depthMap, 7),
    }


def get_bin(a):
    ba = bin(a)[2:]
    return "0" * (8 - len(ba)) + ba


def getUInt16(arr, ind):
    a = arr[ind]
    b = arr[ind + 1]
    return int(get_bin(b) + get_bin(a), 2)


def getFloat32(arr, ind):
    return bin_to_float("".join(get_bin(i) for i in arr[ind : ind + 4][::-1]))


def bin_to_float(binary):
    return struct.unpack("!f", struct.pack("!I", int(binary, 2)))[0]


def parsePlanes(header, depthMap):
    indices = []
    planes = []
    n = [0, 0, 0]

    for i in range(header["width"] * header["height"]):
        indices.append(depthMap[header["offset"] + i])

    for i in range(header["numberOfPlanes"]):
        byteOffset = header["offset"] + header["width"] * header["height"] + i * 4 * 4
        n = [0, 0, 0]
        n[0] = getFloat32(depthMap, byteOffset)
        n[1] = getFloat32(depthMap, byteOffset + 4)
        n[2] = getFloat32(depthMap, byteOffset + 8)
        d = getFloat32(depthMap, byteOffset + 12)
        planes.append({"n": n, "d": d})

    return {"planes": planes, "indices": indices}


def computeDepthMap(header, indices, planes):

    v = [0, 0, 0]
    w = header["width"]
    h = header["height"]

    depthMap = np.empty(w * h)

    sin_theta = np.empty(h)
    cos_theta = np.empty(h)
    sin_phi = np.empty(w)
    cos_phi = np.empty(w)

    for y in range(h):
        theta = (h - y - 0.5) / h * np.pi
        sin_theta[y] = np.sin(theta)
        cos_theta[y] = np.cos(theta)

    for x in range(w):
        phi = (w - x - 0.5) / w * 2 * np.pi + np.pi / 2
        sin_phi[x] = np.sin(phi)
        cos_phi[x] = np.cos(phi)

    for y in range(h):
        for x in range(w):
            planeIdx = indices[y * w + x]

            v[0] = sin_theta[y] * cos_phi[x]
            v[1] = sin_theta[y] * sin_phi[x]
            v[2] = cos_theta[y]

            if planeIdx > 0:
                plane = planes[planeIdx]
                t = np.abs(
                    plane["d"]
                    / (
                        v[0] * plane["n"][0]
                        + v[1] * plane["n"][1]
                        + v[2] * plane["n"][2]
                    )
                )
                depthMap[y * w + (w - x - 1)] = t
            else:
                depthMap[y * w + (w - x - 1)] = 9999999999999999999.0
    return {"width": w, "height": h, "depthMap": depthMap}


# see  https://stackoverflow.com/questions/56242758/python-equivalent-for-javascripts-dataview
# for bytes-parsing reference

# see https://github.com/proog128/GSVPanoDepth.js/blob/master/src/GSVPanoDepth.js
# for overall processing reference

# Base64 string from request to:
# https://maps.google.com/cbk?output=xml&ll=45.508457,-73.532738&dm=1
# edit long and lat
s = "eJzt2gt0FNUdx_FsQtgEFJIQiAlvQglBILzktTOZ2YitloKKD6qAFjy2KD5ABTlqMxUsqICcVqqC1VoUqS34TkMhydjaorYCStXSKkeEihQoICpUFOzuJruZO4_dmdmZe2fY3_cc4RCS-L_z-c_sguaNy8rKzgrkZSGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBCbgsFgB9YzIFYFo_wdsAAZWbC5DliATCwYVPhjATKsYNC0f5s2baiNhagUDFrzb47aeMjVgkF7_liC06JgWv7YAX-n1rfjjx3wbVp-m_5YAV_mpH-bPGpjI4dy1h8L4Lcc9scC-Cyn_bEA_sq6vzF_zB8b4Ktc8McC-Cg3_LEAvkmH3wF_LIBfcskfC-CTHH37r_DHAvgj1_yxAL7IPX8sgB9y0R8L4IPc9McCeD9X_bEAns9dfyyA13PZHwvg8Rz11_LnFVI7SVZWO2UU_71-7jTybwd_67nuT28B4G8j-Gd2LvsXFtJbAPjbyLq_MT_8_RcFf1oLAH8bwd9fFRQUOPr9aPhTWoDT378glqPfEv4-qSCRo98W_v6owM_-dBYA_jaCvz_ytz-VBYC_jeDvsfprP1SeRd0_yVfA39W0_uV0_R393z_gbzX42w3-1rP-8g9_d9P4D4C_yeBvOfhTr7Q06W_D33Z-8Y-l-ABBrvYf4B9_LX_Cf6iTQxsFf8vBn3qp_FULAH_T-cq_dQHgr1v37t0tfgX8LUfJf6hp_-7KLB4G_paj5W96IL_5d9Yp-VeY9j839qPX_I35k_zxT9d_2LDmn3v06NH6wdPBP_kCkP4jR44s7T8y1pCWRkeL_2JI1L9Xr14K_16tpT0-e_8ePUj_jq2d3v6juUhRxNL-vZIV8Q-Hwwr_0YO02R2fhf-w-M8a_45kp4l_GVncv8xs5eWRHxT-0Y_1S6T8TOvjwz_NdP1LkhXDN_zdLjqVR_5R-Ot9ijZz48PffmdF0_XvZjtDTl3_Ir3OUhcZtahrJL0z0PIfWl1dPSqWrv-YWB70P6O1Tt9qqahoYLwuXXT9E5e-p8V0QWMp_I2cI3VqLqv5M7oqa9tWcZb48QJG_n2jFTdX0ru1qip7_pWVY6OFolVWVtacE68y5h_5UKUgCGr_wZr68Txf0jpQ_BwjonOS_n365ChqTxbIVpZzpiLlZYoVCASIX8eucGIXdP31bmA9LnVdOnXS0YwX91d9WCT2RGUejTwLmZF_RUVFbl9FxfFK7PkrX-IqiWL-Le9lVP6xz-5NVBVpRLRiorMj5eYS_sb47SPnJv1ziA04k7xmigun3YNOhLvunTtQ8bRIUSfDRN1vrSVvqyiZeyr_6GWraC43Wusm2PJXvcnppyjm3wxbpfKvimsXG9TMHq1Pczk66ehr_VUroLmAqquoswjKWl8p3MjI2wK7Kf9EFcpNsOOv8z63Kn5Hx_xbPFX-KdUT8HruSfR1_bUPgRRLYGIR9NfC9F4kdTZUN8Ge0j83d7je1YwsgQ1_o9tXk7E_YZ7ihk_ysp9I199gA1IugY1V0C0lcnr3ujX_WDpLYN1f9Q7CvD8pbsU9hb6hf47ey4ClLdDZBbPLQIncir_OElj11zFsKXFvJz6i8rfJnlo_mb_xQ8DyFljcCPe1tRn4a7ESS2DRn3jvoLsAirtc7W8d3QC_vfrcyfxzkj4E0toCz2Xi9lctgSX_FErq76_ytwOvp69z7hT-KR8CBlvguzWw5h_Ngn9Kp-bv2PprZ_xT65vwzzHzEPD_08DAP3JR0vW3I-eEvxl9c_5mHwJ-fh4Y-xttgCl-W3IO-JvDD5j1t7MCvtqE_Pwk_vorkNrfJn6stPxN61vwz7H0OmB2GbyyDfn5mg0g_HU2IIW_7l8bWci2vwX8gDV_-w8BK1HxVhf1z49cAWN_zQYk9Vd-4nCbq2DL35q-VX8aK0BBW1vcP1bCP1tdUn-jN4o6mVsJy_5W8QM2_F1fAbepdSP8m5dAq0-sgFXyVCXbADv6Jg9ux9_VFXCV2TCtv3EOoqfyzzHtbws_YNvfvRVwzzhZVvzdWQGjy2zG38ZzP559f_UKOLQDbgknz6K_GyuQZAGs6Fs8eFr-mh3IIH_HV8D4EifzTws_4IC_egXS3QHnbc1ky9_ZFbBx4dO0j-aEv2YHMsffwRVIx94mfsA5f8d2wEFUC6Xh79QK2MZP6-BO-mt2wMYSOORptfT8HdkBW_bp4Qec99cuQYb4p70D1vGdOLgr_tolML0FTpzJRs74p7cDVuwdO7h7_va2wLGDWcs5f_s7QJs-ltv-eluQbA2cPZ3pnPW3twS06WPR8TfcBM0quHBEM7ngb3kJktC7d3Da_qly76RJc8vfyha0XgQK7vHIQdm5x3P_xLq5ym9yD3JoeGuCfzQ6_im2gcnJ4R-Nhb8mJicnJmCtD3_qEROw1oc_9YgJWOvDn3rEBKz14U89YgLW-vCnHjEBa334U4-YgLU-_KlHTMBaH_7UIyZgrc_K392__jcbk6MTE7DWhz_1iAlY68OfesQErPXhTz1iAtb68KceMQFrffhTj5iAtT78qUdMwFof_tQjJmCtD3_qEROw1oc_9YgJWOvDn3rEBKz14U89YgLW-vCnHjEBa334U48cgTU_Q3825srYnJ0YgTU__KlHjMCaH_7UI0ZgzQ9_6hEjsOaHP_WIEVjzw596xAis-eFPPWIE1vxs_L3xx3_4w59BxAis-eFPPWIE1vzwpx4xAmt--FOPGIE1P_ypR4zAmh_-1CNGYM0Pf-oRI7Dmhz_1yBky1p8NORGTs3vsAcDkCsA_EfzZxeTs8Ie_okzkh39rmejvkbf_8Ic_i4gZ4M8uJoeHP_wVwZ9dTA4P_0z399ICMDm_R_jhD38mEUPAn1lMDh_IeH-vvPzDH_5MIoaAP7NYHD4aMQT8mcXi8NHIKTLSnw24KhaHj0VMAX9WsTh8LGKKTPP3zOMf_vBnEzEF_FnF4PDNkWNkoD8bb3UMDt8SMQb8GcXg8C0RY2SWv3ce__CHP6PIOTLOnw23JvqHT0TMAX820T98ImKOTPL30OPfM_4MF4D6wT3Ez9LfKw8A2sf20u0Pf_izi5gko_wZaWujfXgiYpJM8ffU7c_W3xsLQPfI3uJn7O-JBaB7Ym_xw5-yv8duf9b-XlgAmsf1Gj9zfw8sAMXDeo6fvT_7BaB3VO_xe8Cf-QZQO6f39L3hz3gBKB3Sgzd_tkf8mW4AnQN6U98z_gz_ayCNw3kUP9tD_gFWK-D6sbyLn-0t_2jkdL7397R9NFdPbztiRH_ye_UFX5Vbx3coYlY_-PuEvTWHz-9q5OQe4fcbuKr0L4CnUp0uTX6f25qKCos3Y33pvRNrCfqxvuIeKUvVBQ0jQy8dv5C7_YQk140qE4-83eepF-Z-wT24W5KXc2XigpsnbdxVvzm0-ZQkDy_sJRZ1v1n4a93vmy5ecTs3ZG_X8M79k0PrF3UNzftGkis79BVnnXw-9P6Yu7l_H5Pk54RuYtuCvsLaBePkg8d3b1pQf1CcW1Ar5F57lN8-OJc__itZvGPKkL6XjNvCn6qrlee8Wyqurb5OXpW_vemSPuWNt71WUBN8f0moYO_chuD_JPny1eXi2ZMWhW6pq-BrX5fknPMGidftnh5aOvylhkOHJXluTkfxH5-WC7vHjxM6S8P5rhUrxQtH1cqzO-1r_OxnbRqrpn5P3DbuDuHXt11affmCjvzkSavDnz8_T5i0eHH1-Y915jeWXCRW1LXhpq96gbvlkCQLh7qIQnZJaOs5O7hv9knyd0b1jcw_ivt0wmBueGSeV7qVicOO3yEf2XF-de23X2zo0P7l8DfTa7i3nsjj978nyVPaDxWv--JYqG7UWu6uI5J84vVssfc7S7gfHdjDf_fqWrlnzzXiwH43yBc98Jdq4doZDbMW7ArnPXkF94fupfz1b0ry2qfGiOUFU7mTg5bxA6-S5Jo3ponbP-rIHdh4Fv_xNknu-dYocdn6WfKkvZub_jOxd2P9_iPhpaHb5SfvW9j0xtbixp-ce1icemxE6Muc5dyrX0jyhyfyxPlPZ_GLd57kBr0iySsmni3-MHsPd2LgyYZ7XpPkZy6bL55x_ZpN0z7N4St2SnL_2lzxq9_dKry54ZdN78jLuKpFi8Rrjrbnp67b1rhpca28_IKnxaG_HTj2uaPjG_ZH9mdhzUcCt6eSG_O3eu6rA5HzF58SpoXncdMmzGl8dZEk3_f0LeJD22bLby1ZX716xIKGrEVbw48-_CB39d7_chv-KcmPbn1PuC1vjsBNXNc0uHAh9_gnPcWmLl0aTn18H79wpiSPLXpC-NOPV4cOX5zVUHVSklcW7xBKtrfj31-6heeX18qXzd0nHp5ZyAtlsxpXXC_JM2pfFIuXLOS4wjHcVZ9J8rEzy8Qb7_6aO1BXyq9_UZLnyJeLj7w0R9jz0Nrq-9_syn__vZlC0Q2z5WObn21a1K174_3zDof3DPhNw_qartWTv75LLlp-hfBo2XNjz7t3PP_1s5K8ZcXjQocr53NjpD3c0A8j86z5l9D5gUF8Xtk6vtfOWnnSlQPCo_94KdfuyM9Db38pyatu3iB-_uS73Auz2_HhP0vyzG4jxKcmb-Rq9q0MTYrsW1Hdw-K-D-7hz19X3zj-xlp5SoUY3lA_ketdsJM7GLkfHzv3A-Guv-fzB7aM5JetjJxv-kLx6ISXN065cwI_a70kZxVdKVx7sIo_OKy0cfUvJPnWxmvCcu-e_FUzahse3yzJ9bPXiHN2_GTTK5_Mb_xBxOPolEeqZxQIPBd4g__kzlo5f9op8YwdS7mbJr7LleyS5HvXfSnsWjVHvrXgmeqbLvxpw6G9H4n_Bz8_xLw"
# decode string + decompress zip
depthMapData = parse(s)
# parse first bytes to describe data
header = parseHeader(depthMapData)
# parse bytes into planes of float values
data = parsePlanes(header, depthMapData)
# compute position and values of pixels
depthMap = computeDepthMap(header, data["indices"], data["planes"])
# process float 1D array into int 2D array with 255 values
im = depthMap["depthMap"]
im[np.where(im == max(im))[0]] = 255
if min(im) < 0:
    im[np.where(im < 0)[0]] = 0
im = im.reshape((depthMap["height"], depthMap["width"])).astype(int)
# display image
plt.imshow(im)
plt.show()
