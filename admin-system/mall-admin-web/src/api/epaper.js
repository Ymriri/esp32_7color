import request from '@/utils/request'


export function getEpaperSetting() {
  return request({
    url: '/epaper/epaperUserSetting/get',
    method: 'get',
  })
}

export function updateEpaperUserSettting(data) {
  return request({
    url: '/epaper/epaperUserSetting/update/1',
    method: 'post',
    data: data
  })
}

export function deleteFlash(id) {
  return request({
    url: '/flash/delete/' + id,
    method: 'post'
  })
}


export function getOriginalList(data) {
  return request({
    url: '/epaper/epaperOriginal/list',
    method: 'get',
    params: data
  })
}

export function getOriginalPush() {
  return request({
    url: '/epaper/epaperOriginal/push',
    method: 'get',
  })
}

export function postOriginalPush(data) {
  return request({
    url: '/epaper/epaperOriginal/push',
    method: 'post',
    data: data
  })
}

export function getPicList(date) {
  return request({
    url: '/epaper/epaperPic/allList',
    method: 'get',
    params: date
  })
}

export function createOriginal(data) {
  return request({
    url: '/epaper/epaperOriginal/create',
    method: 'post',
    data: data
  })
}


export function updateFlash(id, data) {
  return request({
    url: '/flash/update/' + id,
    method: 'post',
    data: data
  })
}

