document.addEventListener('DOMContentLoaded', function () {
  // nav menu
  const menus = document.querySelectorAll('.side-menu');
  M.Sidenav.init(menus, { edge: 'right' });
  // add recipe form
  const forms = document.querySelectorAll('.side-form');
  M.Sidenav.init(forms, { edge: 'left' });
});

const recipeContainer = document.querySelector('.recipes');
recipeContainer.addEventListener('click', evt => {
  if (evt.target.tagName === 'I') {
    const diet = evt.target.getAttribute('data-diet');
    const changeItem = evt.target.getAttribute('data-id');    
    const dataMealDay = evt.target.getAttribute('data-meal-day');
    const dataMealTime = evt.target.getAttribute('data-meal-time');

    const requestJson = localStorage.getItem("mealJson")

    loadRecipes(diet, dataMealDay, dataMealTime, changeItem, requestJson);
  }
});
