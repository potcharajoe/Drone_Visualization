/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  Button
} from 'react-native';

import _ from 'lodash';
import MapView from 'react-native-maps';
import axios from 'axios';
import SocketIO from 'socket.io-client'

// let configApi = 'http://158.108.137.193:9090/api'

let io = SocketIO('http://192.168.8.20:9090', {jsonp:false})
let io1 = SocketIO('http://192.168.8.11:9090', {jsonp:false})
let io2 = SocketIO('http://192.168.8.12:9090', {jsonp:false})
let io3 = SocketIO('http://192.168.8.13:9090', {jsonp:false})
// let io = SocketIO('http://158.108.137.193:9090', {jsonp:false})

export default class Drone_visualization extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showText: true,
      annotate: 'My Location :D',
      region: {
        latitude: 13.8463,
        longitude: 100.5687,
        latitudeDelta: 0.0922,
        longitudeDelta: 0.0421,
      },
      markers: {
        1: {
          latlng:{
            latitude:13.9,
            longitude:100.8
          },
          title:'Station',      
          description:'position of station',
          img:''
        },
        2 : {
          latlng:{
            latitude:13.9,
            longitude:100.8
          },
          title:'Drone1',      
          description:'position of station',
          img:''
        },
        3: {
          latlng:{
            latitude:13.9,
            longitude:100.8
          },
          title:'Drone2',
          description:'position of station',
          img:''
        },
        4: {
          latlng:{
            latitude:13.9,
            longitude:100.8
          },
          title:'Drone3',
          description:'position of station',
          img:''
        },
        5: {
          latlng:{
            latitude:13.9,
            longitude:100.8
          },
          title:'Destination',
          description:'position of station',
          img:''
        }
      },
      polylines:{
        1:{
              latitude:13.9,
            longitude:100.8
          },
        2:{
          latitude:13.9,
            longitude:100.8
          },
        3:{
              latitude:13.9,
            longitude:100.8
          },
        4:{
              latitude:13.9,
            longitude:100.8
          },
        5:{
              latitude:13.9,
            longitude:100.8
          }
      },
      allpath:{1: true, 3: true, 2: false},
      used:{
        1:{
              latitude:13.9,
            longitude:100.8
          },
        2:{
          latitude:13.9,
            longitude:100.8
          },
        3:{
              latitude:13.9,
            longitude:100.8
          }
      },
      connected:{
        1:{
              latitude:13.9,
            longitude:100.8
          },
        2:{
          latitude:13.9,
            longitude:100.8
          },
        3:{
              latitude:13.9,
            longitude:100.8
          }
      }
    };
  }

  setWindow(pos){
    const lat = pos.coords.latitude
    const lon = pos.coords.longitude
    // const acc = pos.coords.accuracy
    // const oneDegLatInMeters = 111320
    // const circumference = (40075/360)*1000
    // const latDelta = acc * (1 / (Math.cos(lat) * circumference))
    // const lonDelta = (acc / oneDegLatInMeters)
    this.setState({
      region:{
        latitude: lat,
        longitude: lon,
        latitudeDelta: 0.0922,
        longitudeDelta: 0.0421,
      }
    })
  }    

  componentDidMount(){
    navigator.geolocation.getCurrentPosition(
          pos => this.setWindow(pos)
        )
    io.on('station', (response)=>{
      // console.log(response)
      this.setState({
          markers: {
            ...this.state.markers,
            1: {
              latlng:{
                latitude:response.lat,
                longitude:response.lon
              },
              title:'Station',      
              description:'lat : ' + response.lat + '   lon : ' + response.lon,
              img:require('./src/img/station.png')
            }
          },
          polylines:{
            ...this.state.polylines,
            1:{
              latitude:response.lat,
              longitude:response.lon
            }
          }
        }
        )
    })
    io1.on('drone1', (response)=>{
      // console.log(response)
              this.setState({
          markers: {
            ...this.state.markers,
            2: {
              latlng:{
                latitude:response.lat,
                longitude:response.lon
              
              },
              title:'Drone1',      
              description:'lat : ' + response.lat + '   lon : ' + response.lon,
              img:require('./src/img/drone_pin.png')
            }
          },
          polylines:{
            ...this.state.polylines,
            2:{
                latitude:response.lat,
                longitude:response.lon
              
            }
          }
        })
    })
    io2.on('drone2', (response)=>{
      // console.log(response)
      this.setState({
          markers: {
            ...this.state.markers,
            3: {
              latlng:{
                latitude:response.lat,
                longitude:response.lon
              },
              title:'Drone2',  
              description:'lat : ' + response.lat + '   lon : ' + response.lon,
              img:require('./src/img/drone_pin.png')
            }
          },
          polylines:{
            ...this.state.polylines,
            3: {
              latitude:response.lat,
              longitude:response.lon
            }
          }
        })
    })
    io3.on('drone3', (response)=>{
      // console.log(response)
      this.setState({
          markers: {
            ...this.state.markers,
            4: {
              latlng:{
                latitude:response.lat,
                longitude:response.lon
              },
              title:'Drone3',      
              description:'lat : ' + response.lat + '   lon : ' + response.lon,
              img:require('./src/img/drone_pin.png')
            }
          },
          polylines:{
            ...this.state.polylines,
            4: {
              latitude:response.lat,
              longitude:response.lon
            }
          }
        })
    })
    io.on('destination', (response)=>{
      // console.log(response)
      this.setState({
          markers: {
            ...this.state.markers,
            5: {
              latlng:{
                latitude:response.lat,
                longitude:response.lon
              },
              title:'Destination',      
              description:'lat : ' + response.lat + '   lon : ' + response.lon,
              img:require('./src/img/destination.png')
            }
          },
          polylines:{
            ...this.state.polylines,
            5:{
              latitude:response.lat,
              longitude:response.lon
            }
          }
        })
    })
    io.on('trace', (response)=>{
      // console.log(response);
        this.setState({
            used:{},
            connected:{}
          })
        this.setState({
          allpath:response,
          used:{
            ...this.state.used,
            0:this.state.polylines[1]
          },
          connected:{
            ...this.state.connected,
            0:this.state.polylines[1]
          }
        })
        let c = {}
        let nc = {}
        _.mapKeys(this.state.allpath,(value,key)=>{
          console.log(this.state.polylines)
          if (+key == 3){
            c[key] = this.state.polylines[+key+1]
            nc[key] = this.state.polylines[+key+1]
          }
          else if (value){
            c[key] = this.state.polylines[+key+1]
          }
          else if (!value){
            nc[key] = this.state.polylines[+key+1]
          }
        })
        this.setState({
          used:{
            ...this.state.used,
            ...c,
            5:this.state.polylines[5]
          },
          connected:{
            ...this.state.connected,
            ...nc,
            5:this.state.polylines[5]
          }
        })
    })
  }

  onRegionChange(region) {
    console.log(region)
    this.setState({
      region,
    });
  }

  printStuffs(){
    console.log(this.state.used)
  }

  // <MapView.Polyline 
  //             coordinates = {[{latitude:13.84668,longitude:100.56563},{latitude:13.8467865,longitude:100.5660955},{latitude:13.8472410,longitude:100.5659489}]}
  //             strokeColor='#37BF2A'
  //             strokeWidth = {2}
  //             lineDashPattern = {[2,3]}
  //           />

  render(){
    console.log(this.state.polylines)
    let second = true;
    // console.log(Object.values(this.state.markers));
    return (
      <View style={{flex:1}}>
      <MapView style={{flex:1}}
        region={this.state.region}
        showsUserLocation = {true}
        showsMyLocationButton = {true}
        loadingEnabled = {true}
        onRegionChange={ (x)=>this.onRegionChange(x)}
        onPress={()=>this.printStuffs()}
      >
        {Object.values(this.state.markers).map(marker => (
        <MapView.Marker
            key = {marker.title}
            coordinate={marker.latlng}
            title={marker.title}
            description={marker.description}
            image={marker.img}
            />
          ))} 
          <MapView.Polyline 
              coordinates = {Object.values(this.state.used)}
              strokeColor='#37BF2A'
              strokeWidth = {2}
            />
            <MapView.Polyline 
              coordinates = {Object.values(this.state.connected)}
              strokeColor='#37BF2A'
              strokeWidth = {2}
              lineDashPattern = {[2,3]}
            /> 
        </MapView>
        </View>
    );
  }

}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  map: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
});

AppRegistry.registerComponent('Drone_visualization', () => Drone_visualization);