let $ = mdui.$;

window.authdata = {
    'host':null,
    'talknet':null
}

function authService(url) {
    $.ajax({
        method: 'GET',
        url: url + '/api/info',
        dataType: 'json',
        success: (data, text, xhr) => {
            alert(data)
            let talknet = data['service']['talknet']
            window.authdata = {
                'host':url,
                'talknet':talknet
            }
        },
        error: (err, xhr) => {
            alert('Error')
        }
    })
}