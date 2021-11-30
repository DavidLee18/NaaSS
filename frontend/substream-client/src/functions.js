import store from './store';


export const subscribe = () => changeSubscribingState(true);

export const unsubscribe = () => changeSubscribingState(false);

//vuex dispatch를 간단하게 하기 위한 helper function
const changeSubscribingState = subscribing => store.dispatch('editProfile', { subscribing }).catch(console.error);

//http response status가 정상 응답 범위에 있는지 판별하는 함수
export const isOk = status => status >= 200 && status < 300;

//http 요청 및 vuex dispatch마다 생길 수 있는 에러를 처리하는 함수
export const handleError = error => {
  if(!error) return;
  store.dispatch('unsetError');
  if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      // console.error(`\\response data: ${JSON.stringify(error.response.data)}`);
      // console.error(`\\response status: ${error.response.statusText} (${error.response.status})`);
      // console.error(`\\response headers: ${JSON.stringify(error.response.headers)}`);

      // store.dispatch('setError', JSON.stringify(error.response.data));
      if(error.response.data.detail === 'Incorrect username or password') {
        store.dispatch('setError', 'E-mail이나 비밀번호가 올바르지 않습니다');
      }
  } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      // console.error(`\\request: ${JSON.stringify(error.request)}`);

      // store.dispatch('setError', error.message);
  } else {
      // Something happened in setting up the request that triggered an Error
      // console.error(`\\message: ${error.message}`);

      // store.dispatch('setError', error.message);
  }
  // console.error(`\\config: ${JSON.stringify(error.config)}`);
};