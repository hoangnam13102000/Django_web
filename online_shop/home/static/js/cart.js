let btns = document.getElementsByClassName('addtocart')
for (let i = 0; i < btns.length; i++) {
    btns[i].addEventListener('click', function() {
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log(productId)


    })
}
console.log('productId')