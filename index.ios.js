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

import MapView from 'react-native-maps';
import axios from 'axios';

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
      polylines:{},
      used:{
        d1:true,
        d2:true,
        d3:false
      }
    };
  }

  // addLinetoPoint(){
  //   this.setState({
  //     polylines:[...this.state.polylines,{ latitude: 37.785834, longitude: -122.406417 }]
  //   })
  // }

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


  componentWillMount(){
    navigator.geolocation.getCurrentPosition(
          pos => this.setWindow(pos)
        )
    setInterval( ()=>{
      // axios.get('http://localhost:9090/api/station')
      axios.get('http://158.108.139.33:9090/api/station')
        .then(response => {
          console.log(response.data.lat)
          console.log(response.data.lon)
          this.setState({
          markers: {
            ...this.state.markers,
            1: {
              latlng:{
                latitude:response.data.lat,
                longitude:response.data.lon
              },
              title:'Station',      
              description:'position of station',
              img:require('./src/img/station.png')
            }
          },
          polylines:{
            ...this.state.polylines,
            1:{
              latitude:response.data.lat,
              longitude:response.data.lon
            }
          }
        }
        )}
      );
      // axios.get('http://localhost:9090/api/point1')
      axios.get('http://158.108.139.33:9090/api/point1')
        .then(response => {
          console.log(response.data.lat/10000000)
          console.log(response.data.lon/10000000)
          this.setState({
          markers: {
            ...this.state.markers,
            2: {
              latlng:{
                latitude:response.data.lat/10000000,
                longitude:response.data.lon/10000000
              },
              title:'Drone1',      
              description:'position of point1',
              img:require('./src/img/drone_pin.png')
            }
          },
          polylines:{
            ...this.state.polylines,
            2:{
              latitude:response.data.lat/10000000,
              longitude:response.data.lon/10000000
            }
          }
        })
      }
      );
      // axios.get('http://localhost:9090/api/point2')
      axios.get('http://158.108.139.33:9090/api/point2')
        .then(response => {
          console.log(response.data.lat/10000000)
          console.log(response.data.lon/10000000)
          this.setState({
          markers: {
            ...this.state.markers,
            3: {
              latlng:{
                latitude:response.data.lat/10000000,
                longitude:response.data.lon/10000000
              },
              title:'Drone2',      
              description:'position of point2',
              img:require('./src/img/drone_pin.png')
            }
          },
            polylines:{
              ...this.state.polylines,
            3: {
              latitude:response.data.lat/10000000,
              longitude:response.data.lon/10000000
            }
          }
        })
        }
      );
      // axios.get('http://localhost:9090/api/point3')
      axios.get('http://158.108.139.33:9090/api/point3')
        .then(response => {
          console.log(response.data.lat/10000000)
          console.log(response.data.lon/10000000)
          this.setState({
          markers: {
            ...this.state.markers,
            4: {
              latlng:{
                latitude:response.data.lat/10000000,
                longitude:response.data.lon/10000000
              },
              title:'Drone3',      
              description:'position of point3',
              img:require('./src/img/drone_pin.png')
            }
          },
          polylines:{
            ...this.state.polylines,
            4: {
              latitude:response.data.lat/10000000,
              longitude:response.data.lon/10000000
            }
          }
        })
        }
      );
      // axios.get('http://localhost:9090/api/destination')
      axios.get('http://158.108.139.33:9090/api/destination')
        .then(response => {
          console.log(response.data.lat)
          console.log(response.data.lon)
          this.setState({
          markers: {
            ...this.state.markers,
            5: {
              latlng:{
                latitude:response.data.lat,
                longitude:response.data.lon
              },
              title:'Destination',      
              description:'position of destination',
              img:require('./src/img/destination.png')
            }
          },
          polylines:{
            ...this.state.polylines,
            5:{
              latitude:response.data.lat,
              longitude:response.data.lon
            }
          }
        })
        }
      ); 
      }, 1000)
    }
    

  // componentDidMount(){
  //   setInterval( ()=>{
  //     this.setState({
  //       markers: {
  //         ...this.state.markers,
  //         1:{
  //           latlng:{
  //             latitude:this.state.markers[1].latlng.latitude,
  //             longitude:this.state.markers[1].latlng.longitude+0.0001
  //           },
  //           title:'Station',
  //           description:'position of station'
  //         }
  //       }
  //     })
  //     }, 5000)
  // }


  onRegionChange(region) {
    console.log(region)
    this.setState({
      region,
    });
  }

  printStuffs(){
    console.log(this.state.markers)
  }


  render(){
    let second = true;
    // console.log(Object.values(this.state.image));
    delete this.state.polylines[3];
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
              coordinates = {Object.values(this.state.polylines)}
              strokeColor='#37BF2A'
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
