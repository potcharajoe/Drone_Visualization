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
      annotate: 'My Locaition :D',
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
          description:'position of station'
        },
        2 : {
          latlng:{
            latitude:13.9,
            longitude:100.8
          },
          title:'Drone1',      
          description:'position of station'
        },
        3: {
          latlng:{
            latitude:13.9,
            longitude:100.8
          },
          title:'Drone2',
          description:'position of station'
        },
        4: {
          latlng:{
            latitude:13.9,
            longitude:100.8
          },
          title:'Drone3',
          description:'position of station'
        },
        5: {
          latlng:{
            latitude:13.9,
            longitude:100.8
          },
          title:'Destination',
          description:'position of station'
        }
      }
    };
  }

  setWindow(pos){
    const lat = pos.coords.latitude
    const lon = pos.coords.longitude
    const acc = pos.coords.accuracy
    const oneDegLatInMeters = 111320
    const circumference = (40075/360)*1000
    const latDelta = acc * (1 / (Math.cos(lat) * circumference))
    const lonDelta = (acc / oneDegLatInMeters)

    this.setState({
      region:{
        latitude: lat,
        longitude: lon,
        latitudeDelta: latDelta,
        longitudeDelta: lonDelta,
      }
    })
  }

  componentWillMount() {
      navigator.geolocation.getCurrentPosition(
          pos => this.setWindow(pos)
        )
      axios.get('http://localhost:9090/api/')
        .then(response => {
          // console.log(response.data.lat)
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
            }
          }
        })}
      );
      axios.get('http://localhost:9090/api/')
        .then(response => this.setState({
          markers: {
            ...this.state.markers,
            2: {
              latlng:{
                latitude:200,
                longitude:200
              },
              title:'Drone1',      
              description:'position of station',     
            }
          }
        })
      );
      axios.get('http://localhost:9090/api/')
        .then(response => this.setState({
          markers: {
            ...this.state.markers,
            3: {
              latlng:{
                latitude:200,
                longitude:200
              },
              title:'Drone2',      
              description:'position of station',     
            }
          }
        })
      );
      axios.get('http://localhost:9090/api/')
        .then(response => this.setState({
          markers: {
            ...this.state.markers,
            4: {
              latlng:{
                latitude:200,
                longitude:200
              },
              title:'Drone3',      
              description:'position of station',     
            }
          }
        })
      );
      axios.get('http://localhost:9090/api/')
        .then(response => this.setState({
          markers: {
            ...this.state.markers,
            5: {
              latlng:{
                latitude:200,
                longitude:200
              },
              title:'Destination',      
              description:'position of station',     
            }
          }
        })
      );  
    }

  onRegionChange(region) {
    console.log(region)
    this.setState({
      region,
    });
  }


  render() {
    console.log(Object.values(this.state.markers))
    return (
      <View style={{flex:1}}>
      <MapView style={{flex:1}}
        region={this.state.region}
        showsUserLocation = {true}
        showsMyLocationButton = {true}
        loadingEnabled = {true}
        onRegionChange={ (x)=>this.onRegionChange(x)}
      >
        {Object.values(this.state.markers).map(marker => (
        <MapView.Marker
            key = {marker.title}
            coordinate={marker.latlng}
            title={marker.title}
            description={marker.description}
            />
          ))}  
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
