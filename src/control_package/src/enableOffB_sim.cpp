#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/SetMode.h>
#include <mavros_msgs/State.h>
#include <iostream>
#include <string>

mavros_msgs::State current_state;
void state_cb(const mavros_msgs::State::ConstPtr& msg){
    current_state = *msg;
}

geometry_msgs::PoseStamped targetPose;
void get_Pos(const geometry_msgs::PoseStamped::ConstPtr& msg2){
  targetPose=*msg2;
}

int main(int argc, char **argv)
{

// std::string paramString;
// double xSetPos;
// double ySetPos;
// double zSetPos;


   //Parse arguments: Input arguments are x,y,z co-ordinates of target waypoint:

  //  if (argc>0){
   //
  //    xSetPos= atof(argv[1]);
  //    ySetPos= atof(argv[2]);
  //    zSetPos= atof(argv[3]);
   //
  //  }
   //
  //  // Get the rosparam from the parameter server:
  //  ros::param::get("targetWaypoint", paramString);
   //
  //  std::cout<<" The param received is"<<paramString<<std::endl;
   //
  //  // Create a PoseStamped message:
  //  geometry_msgs::PoseStamped targetPose;
   //
  //  targetPose.pose.position.x = xSetPos;
  //  targetPose.pose.position.y = ySetPos;
  //  targetPose.pose.position.z = zSetPos;




    ros::init(argc, argv, "offb_node_sim");
    ros::NodeHandle nh;

    ros::Subscriber state_sub = nh.subscribe<mavros_msgs::State>
            ("mavros/state", 10, state_cb);

    ros::Subscriber pose_sub= nh.subscribe("savio/Pose",10,get_Pos);

    ros::Publisher local_pos_pub = nh.advertise<geometry_msgs::PoseStamped>
            ("mavros/setpoint_position/local", 10);

    ros::ServiceClient arming_client = nh.serviceClient<mavros_msgs::CommandBool>
            ("mavros/cmd/arming");

    ros::ServiceClient set_mode_client = nh.serviceClient<mavros_msgs::SetMode>
            ("mavros/set_mode");

    //the setpoint publishing rate MUST be faster than 2Hz
    ros::Rate rate(20.0);

    // wait for FCU connection
    while(ros::ok() && current_state.connected){
        ros::spinOnce();
        rate.sleep();
    }



    //send a few setpoints before starting
    for(int i = 100; ros::ok() && i > 0; --i){

        // This is where the desired pose gets published to the Mavros topic: Try intergarting setPos.py with this function:
        local_pos_pub.publish(targetPose);
        ros::spinOnce();
        rate.sleep();
    }



    mavros_msgs::SetMode offb_set_mode;
    offb_set_mode.request.custom_mode = "OFFBOARD";
    //offb_set_mode.request.custom_mode = "OFFBOARD";

    mavros_msgs::CommandBool arm_cmd;
    arm_cmd.request.value = true;

    ros::Time last_request = ros::Time::now();

    // Removing the OFFBOARD mode command from the loop:

        // Check whether the current mode is OFFBOARD
        if( current_state.mode != "OFFBOARD") { //&&
            //(ros::Time::now() - last_request > ros::Duration(15.0))){

            if( set_mode_client.call(offb_set_mode) &&
                offb_set_mode.response.success){
                ROS_INFO("OFFBOARD mode enabled");
            }

            last_request = ros::Time::now();


        }


        // If the current is mode is OFFBOARD then arm the vehicle:
        while(ros::ok()){
            if( current_state.mode=="OFFBOARD" && !current_state.armed &&
                (ros::Time::now() - last_request > ros::Duration(15.0))){
                if( arming_client.call(arm_cmd) &&
                    arm_cmd.response.success){
                    ROS_INFO("Vehicle armed");
                }
                last_request = ros::Time::now();
            }



        // Publish the Target Pose to the set_position_local topic:
        local_pos_pub.publish(targetPose);




        ros::spinOnce();
        rate.sleep();
    }

    return 0;
}
