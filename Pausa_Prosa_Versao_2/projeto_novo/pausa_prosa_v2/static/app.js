let cart=[];
const money=n=>n.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
function add(id,name,price,icon){
  const item=cart.find(i=>i.id===id);
  if(item) item.quantity++;
  else cart.push({id,name,price,icon,quantity:1});
  renderCart();
}
function renderCart(){
  const box=document.querySelector('#cart-items');
  if(!box) return;
  box.innerHTML=cart.length
    ? cart.map(i=>`<div class="cart-line"><span>${i.icon} ${i.name}<br><small>${money(i.price)}</small></span><div><input class="qty" type="number" min="1" value="${i.quantity}" onchange="qty(${i.id},this.value)"><button type="button" class="btn secondary" onclick="removeItem(${i.id})">Remover</button></div></div>`).join('')
    : '<p class="empty">Seu carrinho está vazio.</p>';
  const subtotal=cart.reduce((sum,i)=>sum+i.price*i.quantity,0);
  const subtotalEl=document.querySelector('#subtotal');
  const deliveryEl=document.querySelector('#delivery');
  const totalEl=document.querySelector('#total');
  const countEl=document.querySelector('#count');
  const itemsEl=document.querySelector('#items-json');
  if(subtotalEl) subtotalEl.textContent=money(subtotal);
  if(deliveryEl) deliveryEl.textContent=money(cart.length?5:0);
  if(totalEl) totalEl.textContent=money(subtotal+(cart.length?5:0));
  if(countEl) countEl.textContent=cart.reduce((sum,i)=>sum+i.quantity,0);
  // Atualiza o campo oculto antes de qualquer outra operação.
  if(itemsEl) itemsEl.value=JSON.stringify(cart);
}
function qty(id,value){
  const item=cart.find(i=>i.id===id);
  if(!item) return;
  item.quantity=Math.max(1,Number(value)||1);
  renderCart();
}
function removeItem(id){cart=cart.filter(i=>i.id!==id);renderCart();}
document.addEventListener('DOMContentLoaded',()=>{
  renderCart();
  const form=document.querySelector('form[action*="pedido"]');
  if(form) form.addEventListener('submit',event=>{
    renderCart();
    if(cart.length===0){event.preventDefault();alert('Adicione pelo menos um produto ao carrinho antes de enviar o pedido.');}
  });
});
