let $ = mdui.$;
let P = 'chat' // current page
let C = []     // chat list
let A = null   // current uid
let T = {}     // temp of inputs

let H = {
    '_me': 'http://q2.qlogo.cn/headimg_dl?dst_uin=3206921401&spec=100'
}

SetPage('sign')

String.prototype.nReplace = function (f, e) {
    let reg = new RegExp(f, "g");
    return this.replace(reg, e);
}

function Randomcode(length) {
    let chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    let result = '';
    for (var i = length; i > 0; --i) result += chars[Math.floor(Math.random() * chars.length)];
    return result;
}

function SetPage(to) {
    if ((to == 'chat') && (P != 'chat')) {
        P = 'chat'
        $('#chat').removeClass('mdui-hidden')
        $('#list').removeClass('mdui-hidden')
        $('#setting').addClass('mdui-hidden')
        $('#setmenu').addClass('mdui-hidden')
        $('#signin').addClass('mdui-hidden')
    } else if ((to == 'setting') && (P != 'setting')) {
        P = 'setting'
        $('#chat').addClass('mdui-hidden')
        $('#list').addClass('mdui-hidden')
        $('#setting').removeClass('mdui-hidden')
        $('#setmenu').removeClass('mdui-hidden')
        $('#signin').addClass('mdui-hidden')
    } else if ((to == 'sign') && (P != 'sign')) {
        P = 'sign'
        $('#chat').addClass('mdui-hidden')
        $('#list').addClass('mdui-hidden')
        $('#setting').addClass('mdui-hidden')
        $('#setmenu').addClass('mdui-hidden')
        $('#signin').removeClass('mdui-hidden')
    }
}

function Unlock() {
    $('#ico-chat').removeClass('mdui-hidden')
    $('#ico-create').removeClass('mdui-hidden')
    $('#ico-set').removeClass('mdui-hidden')
}

function Update(uid, info) {
    if (C.includes(uid) == false) return;
    let now = $('#' + uid + '-ls').find('.mdui-list-item-text')
    now.html(info)
}

function CreatNew(title, head, uid) {
    if (C.includes(uid)) {
        console.log('error');
    } else {
        // create chat ui
        let html = document.createElement('div')
        html.id = uid
        html.classList.add('mdui-hidden')
        html.innerHTML = '<div class="page-content mdui-p-x-2"style="height:calc(100vh - 117px - 48px - 42px);"></div>'.nReplace('TITLE', title)
        $('#box').append(html)
        // create list ui
        $('#list').append('<li id="UID-ls" onclick="Activme(\'UID\')" class="mdui-list-item mdui-ripple"><div class="mdui-list-item-avatar"><img src="HEAD"/></div><div class="mdui-list-item-content"><div class="mdui-list-item-title">TITLE</div><div class="mdui-list-item-text mdui-list-item-one-line"></div></div></li>'.nReplace('HEAD', head).nReplace('TITLE', title).nReplace('UID', uid))
        // push to list
        C.push(uid)
        H[uid] = head
    }
}

function Active(uid) {
    if (C.includes(uid) == false) return;
    if (uid == A) return;
    $('#init_box').addClass('mdui-hidden')
    $('#input_box').removeClass('mdui-hidden')
    // chat ui
    $('#' + A).addClass('mdui-hidden')
    $('#' + uid).removeClass('mdui-hidden')
    // inner title
    let list_title = $('#' + uid + '-ls').find('.mdui-list-item-title').html()
    $('#innertitle').html('与 ' + list_title)
    A = uid
}

function Addrecv(uid, text) {
    if (C.includes(uid) == false) return;
    let now = $('#' + uid).find('.page-content')
    now.append('<div class="page-left"><img src="HEAD"/><div class="page-text">TEXT</div></div>'.nReplace('HEAD', H[uid]).nReplace('TEXT', text.nReplace('\n', '<br/>')))
    Update(uid, text)
}

function Addsend(uid, text) {
    if (C.includes(uid) == false) return;
    let now = $('#' + uid).find('.page-content')
    now.append('<div class="page-right"><div class="page-text">TEXT</div><img src="HEAD"/></div>'.nReplace('HEAD', H['_me']).nReplace('TEXT', text.nReplace('\n', '<br/>')))
    Update(uid, text)
}

function Addinfo(uid, info) {
    if (C.includes(uid) == false) return;
    let now = $('#' + uid).find('.page-content')
    now.append('<div class="page-info mdui-text-center mdui-m-t-1"><span>INFO</span></div>'.nReplace('INFO', info))
    Update(uid, info)
}

function Activme(uid) {
    if (C.includes(uid) == false) return;
    if (uid == A) return;
    $('#' + A + '-ls').removeClass('mdui-list-item-active')
    $('#' + uid + '-ls').addClass('mdui-list-item-active')
    Active(uid)
}

function sendmsg() { }

function Keep(uid) {
    if (C.includes(uid) == false) return;
    let now = $('#' + uid).children('.page-content')[0]
    console.log(now);
    let height = now.scrollHeight;
    now.scrollTop = height;
}

function Checkhost() {
    let host = $('#host').val()
    let save = document.getElementById("save").checked
    if (host == '') return

    // ui disabling
    $('#f-pro').removeClass('mdui-invisible')
    $('#next').attr('disabled', '')
    $('#host').attr('disabled', '')
    $('#save').attr('disabled', '')

    authService(
        host,
        () => {
            if (window.authdata['host'] && window.authdata['talknet']) {
                $('#f-card').addClass('mdui-hidden')
                $('#s-card').removeClass('mdui-hidden')
                mdui.snackbar({
                    message: '连接成功',
                    position: 'right-bottom',
                });
            } else {
                $('#f-pro').addClass('mdui-invisible')
                $('#next').removeAttr('disabled')
                $('#host').removeAttr('disabled')
                $('#save').removeAttr('disabled')
                mdui.snackbar({
                    message: '接口不存在',
                    position: 'right-bottom',
                });
            }
        },
        () => {
            $('#f-pro').addClass('mdui-invisible')
            $('#next').removeAttr('disabled')
            $('#host').removeAttr('disabled')
            $('#save').removeAttr('disabled')
            mdui.snackbar({
                message: '接口不存在',
                position: 'right-bottom',
            });
        }
    )
}

function authService(url, sec, err) {
    $.ajax({
        method: 'GET',
        url: url + '/api/info',
        dataType: 'json',
        success: (data, text, xhr) => {
            console.log(data)
            let talknet = data['services']['talknet']
            window.authdata = {
                'host': url,
                'talknet': talknet
            }
            if (sec) sec();
        },
        error: (e, xhr) => {
            console.log('Error')
            if (err) err();
        }
    })
}

function Signin() {
    let name = $('#user').val().nReplace(' ', '')
    let pswd = $('#pswd').val().nReplace(' ', '')
    if ((name == '') || (pswd == '')) {
        mdui.snackbar({
            message: '无效的信息',
            position: 'right-bottom',
        });
    }
    CreatWS(name, pswd)
}

function CreatWS(name, pswd) {
    let namespace = window.authdata['talknet']
    let linking = window.authdata['host'] + namespace

    let socket = io.connect(linking, {
        'auth': {
            'name': name,
            'pswd': pswd
        }
    })

    socket.on('list', function (data) {
        if (data[0] == 'create') {
            $.each(data[1], function (key, value) {
                // list id
                key = value.frid + '';
                CreatNew(value.name, '/api/avatar?uid=' + value.frid, key)
                H[key] = '/api/avatar?uid=' + value.frid
                C.push(key)
            })
        }
    })

    socket.on('message', function (data) {
        Addrecv(data['uid'] + '', data['context'])
    })

    socket.on('connect_error', (error) => {
        mdui.snackbar({
            message: '登录被拒绝',
            position: 'right-bottom',
        });
    });

    socket.on('connect', function () {
        Unlock()
        socket.emit('list')
        SetPage('chat')
        sendmsg = function () {
            let text = $('#input').val()
            if (text == '') return;
            socket.emit('person', {
                'uid': Number(A),
                'context': text
            })
            Addsend(A, text)
            $('#input').val('')
        }
    })
}