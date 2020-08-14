const json = require('../incidents.json')
const _ = require('lodash')
let hashesContainer = {}
let hashesContainer2 = {}

json.tickets.forEach( ticket => {

    let hash = ticket.file_hash.toString();
    if(!hashesContainer[hash]) {
        hashesContainer[hash] = []
        hashesContainer2[hash] = new Set();
    }
    
    hashesContainer[hash].push(ticket.dst_ip)
    hashesContainer2[hash].add(ticket.dst_ip)



})

console.log(hashesContainer)
console.log("----------------------")
console.log(hashesContainer2)