document.addEventListener('DOMContentLoaded', function() {
  // nav menu
  const menus = document.querySelectorAll('.side-menu');
  M.Sidenav.init(menus, {edge: 'right'});
  // add recipe form
  const forms = document.querySelectorAll('.side-form');
  M.Sidenav.init(forms, {edge: 'left'});
});

const recipeContainer = document.querySelector('.recipes');
recipeContainer.addEventListener('click', evt => {
  if(evt.target.tagName === 'I') {
    const id = evt.target.getAttribute('data-id');
    alert(id);
    loadRecipes()
  }
});
