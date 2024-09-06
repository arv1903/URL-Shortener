function generateCode() {
        let ret = '', now = 0;
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        while (now < 6) {
                ret += chars.charAt(Math.floor(Math.random() * chars.length));
                now += 1;
        }
        document.getElementById("short").value = ret;
}

function copyToClipboard(text) {
        navigator.clipboard.writeText("https://mvn.my.id/" + text)
                .then(function () {
                        alert('Copied to clipboard');
                })
                .catch(function (err) {
                        console.error('Unable to copy', err);
                        alert('Failed to copy to clipboard.');
                });
}

function generateQRCode(long, short) {
        var url = 'https://api.qrserver.com/v1/create-qr-code/?data=' + long + '&amp;size=50x50', copyLink = 'copyToClipboard("' + short + '")';
        $('#image').attr('src', url);

        $('#copy').attr('onclick', copyLink);
        $('#whatsapp').attr('href', "whatsapp://send?text=" + "Visit my shortened version of " + long + " : " + "mvn.my.id/" + short);
        $('#twitter').attr('href', "http://twitter.com/share?text=" + "Visit my shortened version of " + long + " : " + "mvn.my.id/" + short);
        $('#line').attr('href', "https://social-plugins.line.me/lineit/share?url=https%3A%2F%2Fline.me%2Fen&text=" + "Visit my shortened version of " + long + " : " + "mvn.my.id/" + short);
        $('#threads').attr('href', "https://threads.net/intent/post?text=" + "Visit my shortened version of " + long + " : " + "mvn.my.id/" + short);
}

function filterURLs() {
        let input = document.getElementById('search');
        let filter = input.value.toUpperCase();
        let urlContainer = document.getElementById("url-container");
        let urlBoxes = urlContainer.getElementsByClassName('url-box');

        for (let i = 0; i < urlBoxes.length; i++) {
                let h1 = urlBoxes[i].getElementsByTagName("h1")[0];
                if (h1) {
                        let txtValue = h1.textContent || h1.innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                                urlBoxes[i].style.display = "";
                        } else {
                                urlBoxes[i].style.display = "none";
                        }
                }
        }
}