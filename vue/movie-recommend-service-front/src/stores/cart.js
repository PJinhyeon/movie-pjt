import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCartStore = defineStore('cart', () => {
  const cartItems = ref([])

  const getCart = () => {
    const token = localStorage.getItem('authToken');

    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/movies/cart/',
      headers: {
        Authorization: `Token ${token}`
      }
    })
      .then((res) => {
        // console.log('cartitem list: ', res.data)
        cartItems.value = res.data
      })
      .catch((err) => {
        console.log('에러:', err)
      })
  }

  const addCart = (movieId) => {
    const token = localStorage.getItem('authToken')

    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/movies/cart/',
      headers: {
        Authorization: `Token ${token}`
      },
      data: {
        movie: movieId
      }
    })
      .then((res) => {
        cartItems.value.push(res.data)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const removeCart = function (movieId) {
    const token = localStorage.getItem('authToken')

    axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/movies/cart/${movieId}/`,
      headers: {
        Authorization: `Token ${token}`
      },
    })
      .then((res) => {
        console.log('찜 제거 : ', res.data)
        getCart()
      })
      .catch((err) => {
        console.log(err)
      })
  }



  return { getCart, cartItems, addCart, removeCart }

})