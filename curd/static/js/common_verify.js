/**
 *  author: luobin@donews.com
 *  date: 2018-12-27
 *  time: 02:13
 *  description: 前端验证的一些公用方法
 */

/**
 * IP校验1
 */
function checkIP1(ip) {
    var reSpaceCheck = /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/;
    if (reSpaceCheck.test(ip)) {
        ip.match(reSpaceCheck);
        if (RegExp.$1 <= 255 && RegExp.$1 >= 0
            && RegExp.$2 <= 255 && RegExp.$2 >= 0
            && RegExp.$3 <= 255 && RegExp.$3 >= 0
            && RegExp.$4 <= 255 && RegExp.$4 >= 0) {
            return true;
        } else {
            return false;
        }
    } else {
        return false;
    }
}

/**
 *  端口号校验
 */
function checkPort(str) {
    var parten = /^(\d)+$/g;
    if (parten.test(str) && parseInt(str) <= 65535 && parseInt(str) >= 0) {
        return true;
    } else {
        return false;
    }
}


/**
 *  IP校验
 */
function checkIP(value) {
    var exp = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    var reg = value.match(exp);
    if (reg == null) {
        return false;
    } else {
        return true;
    }
}


/**
 *  mask(子网掩码)校验
 */
function checkMask(mask) {
    obj = mask;
    var exp = /^(254|252|248|240|224|192|128|0)\.0\.0\.0|255\.(254|252|248|240|224|192|128|0)\.0\.0|255\.255\.(254|252|248|240|224|192|128|0)\.0|255\.255\.255\.(254|252|248|240|224|192|128|0)$/;
    var reg = obj.match(exp);
    if (reg == null) {
        return false; //"非法"
    }
    else {
        return true; //"合法"
    }
}

/**
 *  比较两个ip地址的前后，,如果大于，返回1，等于返回0，小于返回-1
 */
function compareIP(ipBegin, ipEnd) {
    var temp1;
    var temp2;
    temp1 = ipBegin.split(".");
    temp2 = ipEnd.split(".");
    for (var i = 0; i < 4; i++) {
        if (temp1[i] > temp2[i]) {
            return 1;
        }
        else if (temp1[i] < temp2[i]) {
            return -1;
        }
    }
    return 0;
}

// 验证IP的正则
var ip_reg = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

// 验证子网掩码的正则
var mask_reg = /^(254|252|248|240|224|192|128|0)\.0\.0\.0|255\.(254|252|248|240|224|192|128|0)\.0\.0|255\.255\.(254|252|248|240|224|192|128|0)\.0|255\.255\.255\.(254|252|248|240|224|192|128|0)$/;

// 验证网段的正则
var segment_reg = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/([0-9]|[1,2][0-9]|3[0-2])$/;

/**
 *　　把IP地址转换成二进制格式
 *　　@param string   ip    待转换的IP的地址
 */
function ip_to_binary(ip) {
    if (ip_reg.test(ip)) {
        var ip_str = "",
            ip_arr = ip.split(".");

        for (var i = 0; i < 4; i++) {
            curr_num = ip_arr[i];
            number_bin = parseInt(curr_num);
            number_bin = number_bin.toString(2);
            count = 8 - number_bin.length;
            for (var j = 0; j < count; j++) {
                number_bin = "0" + number_bin;
            }
            ip_str += number_bin;
        }
        return ip_str;
    }

    return '';
}

/**
 *　　把二进制格式转换成IP地址
 *　　@param string   binary    待转换的二进制　　
 */
function binary_to_ip(binary) {
    if (binary.length == 32) {
        a = parseInt(binary.substr(0, 8), 2);
        b = parseInt(binary.substr(8, 8), 2);
        c = parseInt(binary.substr(16, 8), 2);
        d = parseInt(binary.slice(-8), 2);

        return a + '.' + b + '.' + c + '.' + d;
    }

    return '';
}

/**
 *  根据 掩码位 计算掩码
 */
function calcMask(num) {
    let net_mask = "";
    n = parseInt(num);
    a = (1<<n) - 1;
    b = a.toString(2);
    d = (1<<(32 - n));
    y = d.toString(2).substr(1);
    sanshier = b + y;
    net_mask = parseInt(sanshier.substring(0, 8), 2).toString() + "." + parseInt(sanshier.substring(8, 16), 2).toString() + "." + parseInt(sanshier.substring(16, 24), 2).toString() + "." + parseInt(sanshier.substring(24, 32), 2).toString();
    return net_mask;
}

/**
 * 根据 掩码位 计算可用ip数量
 */
function calcIPNum(num) {
    let ipn = 0;
    n = parseInt(num);
    ipn = Math.pow(2, 32-n) - 2;
    return ipn;
}

/**
 *　　根据子网掩码和网关计算网络地址和广播地址
 *　　@param  string    mask    子网掩码
 *　　@param  string    ip 网关
 */
function get_network_broadcast_addr(mask, ip) {
    network_broadcast = [];
    network_addr = "";

    mask_arr = mask.split(".");
    ip_arr = ip.split(".");

    // 计算IP的网络地址 与(&)运算
    for (var i = 0; i < 4; i++) {
        number1 = parseInt(mask_arr[i]);
        number2 = parseInt(ip_arr[i]);
        network_addr += number1 & number2;
        if (i < 3) {
            network_addr += ".";
        }
    }
    network_broadcast.push(network_addr);

    // 计算广播地址
    // 子掩码后面有几个0，就去掉IP地址后几位再补1
    mask_binary = ip_to_binary(mask);
    gateway_binary = ip_to_binary(ip);

    mask_zero = mask_binary.split(0).length - 1;
    one_number = new Array(mask_zero + 1).join('1'); // IP地址后位补1
    gateway_hou_wei_bu_yi = gateway_binary.slice(0, -mask_zero) + one_number;

    network_broadcast.push(binary_to_ip(gateway_hou_wei_bu_yi));

    return network_broadcast;
}

//  全排列组合算法（两两递归组合）
function doExchange(doubleArrays) {
    var len = doubleArrays.length;
    if (len >= 2) {
        var len1 = doubleArrays[0].length;
        var len2 = doubleArrays[1].length;
        var newlen = len1 * len2;
        var temp = new Array(newlen);
        var index = 0;
        for (var i = 0; i < len1; i++) {
            for (var j = 0; j < len2; j++) {
                temp[index] = doubleArrays[0][i] + '.' + doubleArrays[1][j];
                index++;
            }
        }

        var newArray = new Array(len - 1);
        for (var i = 2; i < len; i++) {
            newArray[i - 1] = doubleArrays[i];
        }
        newArray[0] = temp;

        return doExchange(newArray);

    } else {
        return doubleArrays[0];
    }
}

/**
 *　　获取由网络地址和广播址组成的所有IP组合
 *　　@param  string    network_addr    网络地址
 *　　@param  string    broadcast_addr  广播地址
 *　　@param  string    gateway         网关
 */
function return_ip(network_addr, broadcast_addr, gateway) {
    range = [];
    start = network_addr.split(".");
    end = broadcast_addr.split(".");

    /*// range格式为[[192], [168], [0,1,2...254], [0,1,2...254]]
    for (var i = 0; i < 4; i++) {
        if (start[i] == end[i]) {
            range[i] = [start[i]];
        } else {
            min = Math.min(start[i], end[i]);
            max = Math.max(start[i], end[i]);
            temp = [];
            if (i == 3) min = 199; // 从200起计
            for (var j = min; j <= max; j++) {
                temp.push(j);
            }
            range[i] = temp;
        }
    }*/

    // range格式为[[192], [168], [0,1,2...254], [0,1,2...254]]
    for (var i = 0; i < 4; i++) {
        if (start[i] == end[i]) {
            range[i] = [start[i]];
        } else {
            min = Math.min(start[i], end[i]);
            max = Math.max(start[i], end[i]);
            temp = [];
            for (var j = min; j <= max; j++) {
                temp.push(j);
            }
            range[i] = temp;
        }
    }

    ip_list = doExchange(range);
    ip_list.shift(); // 去掉网络地址
    ip_list.pop(); // 去掉广播地址
    gateway_index = -1;

    // 去掉网关
    for (var k = 0; k < ip_list.length; k++) {
        if (ip_list[k] == gateway) {
            gateway_index = k;
            break;
        }
    }
    if (gateway_index > -1) {
        ip_list.splice(gateway_index, 1);
    }

    return ip_list;
}