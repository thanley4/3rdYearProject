// Tencent is pleased to support the open source community by making ncnn available.
//
// Copyright (C) 2020 THL A29 Limited, a Tencent company. All rights reserved.
//
// Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
// in compliance with the License. You may obtain a copy of the License at
//
// https://opensource.org/licenses/BSD-3-Clause
//
// Unless required by applicable law or agreed to in writing, software distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.

// modified 12-31-2021 Q-engineering

#include "/usr/local/include/ncnn/layer.h"
#include "/usr/local/include/ncnn/net.h"

#include <time.h>
#include <iostream>

#include </usr/local/include/opencv4/opencv2/core/core.hpp>
#include </usr/local/include/opencv4/opencv2/highgui/highgui.hpp>
#include </usr/local/include/opencv4/opencv2/imgproc/imgproc.hpp>
#include <stdio.h>
#include <vector>

#include <stdio.h>
#include <unistd.h>
#include <string>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <iostream>
#include <sstream>
#include <iterator>
#include <fcntl.h>

#pragma clang diagnostic push
#pragma ide diagnostic ignored "EndlessLoop"
#pragma comment (lib, "Ws2_32.lib")

#define PORT 9999

#define BUFFER_SIZE 2048

// 0 : No unneccesary tasks (display image, etc.)
// 1 : Unneccessary tasks (display image, etc.)
#define MARGINAL_GAINS 1

#define SEND_PACKET 1
// 1 : Send Packet

#define USE_CAMERA 0
// 0 : Use .mp4 file
// 1 : Use Gstreamer Camera

#define DRAW_BOXES 1

using namespace std;

ncnn::Net yolov5;

const int target_size = 320;
const float prob_threshold = 0.25f;
const float nms_threshold = 0.45f;
const float norm_vals[3] = {1 / 255.f, 1 / 255.f, 1 / 255.f};

const float total_sensor_height_mm = 2.76f;
const float total_sensor_width_mm = 3.68f;
const int total_sensor_height_pixels = 360;
const int total_sensor_width_pixels = 640;
const float sensor_focal_length_mm = 3.04f;
const float sensor_field_of_view_degrees = 62.2f;

const float object_heights[] = {
    1.72f, 1.05f, 1.6f, 1.125f, 19.0f, 3.8f, 4.0f, 4.0f, 2.0f, 0.6f,
    0.8, 0.8, 1.7, 0.8, 0.2, 0.3, 0.4, 1.9, 0.8, 1.4
};


const char* class_names[] = {
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush"
};

static float object_distance(int object_id, int object_height_pixels)
{
    float object_height_on_sensor_mm = total_sensor_height_mm * object_height_pixels / total_sensor_height_pixels;
    float distance_to_object = (object_heights[object_id] * sensor_focal_length_mm / object_height_on_sensor_mm);
    return distance_to_object;
}

static float object_angle(int x_location)
{
    float angle_to_object = ((x_location - (total_sensor_width_pixels / 2)) * (sensor_field_of_view_degrees / total_sensor_width_pixels));
    return angle_to_object;
}

static float object_width(int object_id, int object_height_pixels, int object_width_pixels)
{
    float object_width_m = (object_width_pixels * object_heights[object_id] / object_height_pixels);
    return object_width_m;
}

struct TIMEVAL
{
    long tv_sec;
    long tv_usec;
};


class YoloV5Focus : public ncnn::Layer
{
public:
    YoloV5Focus()
    {
        one_blob_only = true;
    }

    virtual int forward(const ncnn::Mat& bottom_blob, ncnn::Mat& top_blob, const ncnn::Option& opt) const
    {
        int w = bottom_blob.w;
        int h = bottom_blob.h;
        int channels = bottom_blob.c;

        int outw = w / 2;
        int outh = h / 2;
        int outc = channels * 4;

        top_blob.create(outw, outh, outc, 4u, 1, opt.blob_allocator);
        if (top_blob.empty())
            return -100;

        #pragma omp parallel for num_threads(opt.num_threads)
        for (int p = 0; p < outc; p++)
        {
            const float* ptr = bottom_blob.channel(p % channels).row((p / channels) % 2) + ((p / channels) / 2);
            float* outptr = top_blob.channel(p);

            for (int i = 0; i < outh; i++)
            {
                for (int j = 0; j < outw; j++)
                {
                    *outptr = *ptr;

                    outptr += 1;
                    ptr += 2;
                }

                ptr += w;
            }
        }

        return 0;
    }
};

DEFINE_LAYER_CREATOR(YoloV5Focus)

struct Object
{
    cv::Rect_<float> rect;
    int label;
    float prob;
};

static inline float intersection_area(const Object& a, const Object& b)
{
    cv::Rect_<float> inter = a.rect & b.rect;
    return inter.area();
}

static void qsort_descent_inplace(std::vector<Object>& faceobjects, int left, int right)
{
    int i = left;
    int j = right;
    float p = faceobjects[(left + right) / 2].prob;

    while (i <= j)
    {
        while (faceobjects[i].prob > p)
            i++;

        while (faceobjects[j].prob < p)
            j--;

        if (i <= j)
        {
            // swap
            std::swap(faceobjects[i], faceobjects[j]);

            i++;
            j--;
        }
    }

    #pragma omp parallel sections
    {
        #pragma omp section
        {
            if (left < j) qsort_descent_inplace(faceobjects, left, j);
        }
        #pragma omp section
        {
            if (i < right) qsort_descent_inplace(faceobjects, i, right);
        }
    }
}

static void qsort_descent_inplace(std::vector<Object>& faceobjects)
{
    if (faceobjects.empty())
        return;

    qsort_descent_inplace(faceobjects, 0, faceobjects.size() - 1);
}

static void nms_sorted_bboxes(const std::vector<Object>& faceobjects, std::vector<int>& picked, float nms_threshold)
{
    picked.clear();

    const int n = faceobjects.size();

    std::vector<float> areas(n);
    for (int i = 0; i < n; i++)
    {
        areas[i] = faceobjects[i].rect.area();
    }

    for (int i = 0; i < n; i++)
    {
        const Object& a = faceobjects[i];

        int keep = 1;
        for (int j = 0; j < (int)picked.size(); j++)
        {
            const Object& b = faceobjects[picked[j]];

            // intersection over union
            float inter_area = intersection_area(a, b);
            float union_area = areas[i] + areas[picked[j]] - inter_area;
            // float IoU = inter_area / union_area
            if (inter_area / union_area > nms_threshold)
                keep = 0;
        }

        if (keep)
            picked.push_back(i);
    }
}

static inline float sigmoid(float x)
{
    return static_cast<float>(1.f / (1.f + exp(-x)));
}

static void generate_proposals(const ncnn::Mat& anchors, int stride, const ncnn::Mat& in_pad, const ncnn::Mat& feat_blob, float prob_threshold, std::vector<Object>& objects)
{
    const int num_grid = feat_blob.h;

    int num_grid_x;
    int num_grid_y;
    if (in_pad.w > in_pad.h)
    {
        num_grid_x = in_pad.w / stride;
        num_grid_y = num_grid / num_grid_x;
    }
    else
    {
        num_grid_y = in_pad.h / stride;
        num_grid_x = num_grid / num_grid_y;
    }

    const int num_class = feat_blob.w - 5;

    const int num_anchors = anchors.w / 2;

    for (int q = 0; q < num_anchors; q++)
    {
        const float anchor_w = anchors[q * 2];
        const float anchor_h = anchors[q * 2 + 1];

        const ncnn::Mat feat = feat_blob.channel(q);

        for (int i = 0; i < num_grid_y; i++)
        {
            for (int j = 0; j < num_grid_x; j++)
            {
                const float* featptr = feat.row(i * num_grid_x + j);

                // find class index with max class score
                int class_index = 0;
                float class_score = -FLT_MAX;
                for (int k = 0; k < num_class; k++)
                {
                    float score = featptr[5 + k];
                    if (score > class_score)
                    {
                        class_index = k;
                        class_score = score;
                    }
                }

                float box_score = featptr[4];

                float confidence = sigmoid(box_score) * sigmoid(class_score);

                if (confidence >= prob_threshold)
                {
                    // yolov5/models/yolo.py Detect forward
                    // y = x[i].sigmoid()
                    // y[..., 0:2] = (y[..., 0:2] * 2. - 0.5 + self.grid[i].to(x[i].device)) * self.stride[i]  # xy
                    // y[..., 2:4] = (y[..., 2:4] * 2) ** 2 * self.anchor_grid[i]  # wh

                    float dx = sigmoid(featptr[0]);
                    float dy = sigmoid(featptr[1]);
                    float dw = sigmoid(featptr[2]);
                    float dh = sigmoid(featptr[3]);

                    float pb_cx = (dx * 2.f - 0.5f + j) * stride;
                    float pb_cy = (dy * 2.f - 0.5f + i) * stride;

                    float pb_w = pow(dw * 2.f, 2) * anchor_w;
                    float pb_h = pow(dh * 2.f, 2) * anchor_h;

                    float x0 = pb_cx - pb_w * 0.5f;
                    float y0 = pb_cy - pb_h * 0.5f;
                    float x1 = pb_cx + pb_w * 0.5f;
                    float y1 = pb_cy + pb_h * 0.5f;

                    Object obj;
                    obj.rect.x = x0;
                    obj.rect.y = y0;
                    obj.rect.width = x1 - x0;
                    obj.rect.height = y1 - y0;
                    obj.label = class_index;
                    obj.prob = confidence;

                    objects.push_back(obj);
                }
            }
        }
    }
}

static int detect_yolov5(const cv::Mat& bgr, std::vector<Object>& objects)
{
    int img_w = bgr.cols;
    int img_h = bgr.rows;

    // letterbox pad to multiple of 32
    int w = img_w;
    int h = img_h;
    float scale = 1.f;
    if (w > h)
    {
        scale = (float)target_size / w;
        w = target_size;
        h = h * scale;
    }
    else
    {
        scale = (float)target_size / h;
        h = target_size;
        w = w * scale;
    }

    ncnn::Mat in = ncnn::Mat::from_pixels_resize(bgr.data, ncnn::Mat::PIXEL_BGR2RGB, img_w, img_h, w, h);

    // pad to target_size rectangle
    // yolov5/utils/datasets.py letterbox
    int wpad = (w + 31) / 32 * 32 - w;
    int hpad = (h + 31) / 32 * 32 - h;
    ncnn::Mat in_pad;
    ncnn::copy_make_border(in, in_pad, hpad / 2, hpad - hpad / 2, wpad / 2, wpad - wpad / 2, ncnn::BORDER_CONSTANT, 114.f);

    const float norm_vals[3] = {1 / 255.f, 1 / 255.f, 1 / 255.f};
    in_pad.substract_mean_normalize(0, norm_vals);

    ncnn::Extractor ex = yolov5.create_extractor();

    ex.input("images", in_pad);

    std::vector<Object> proposals;

    // anchor setting from yolov5/models/yolov5s.yaml

    // stride 8
    {
        ncnn::Mat out;
        ex.extract("output", out);

        ncnn::Mat anchors(6);
        anchors[0] = 10.f;
        anchors[1] = 13.f;
        anchors[2] = 16.f;
        anchors[3] = 30.f;
        anchors[4] = 33.f;
        anchors[5] = 23.f;

        std::vector<Object> objects8;
        generate_proposals(anchors, 8, in_pad, out, prob_threshold, objects8);

        proposals.insert(proposals.end(), objects8.begin(), objects8.end());
    }

    // stride 16
    {
        ncnn::Mat out;
        ex.extract("781", out);

        ncnn::Mat anchors(6);
        anchors[0] = 30.f;
        anchors[1] = 61.f;
        anchors[2] = 62.f;
        anchors[3] = 45.f;
        anchors[4] = 59.f;
        anchors[5] = 119.f;

        std::vector<Object> objects16;
        generate_proposals(anchors, 16, in_pad, out, prob_threshold, objects16);

        proposals.insert(proposals.end(), objects16.begin(), objects16.end());
    }

    // stride 32
    {
        ncnn::Mat out;
        ex.extract("801", out);

        ncnn::Mat anchors(6);
        anchors[0] = 116.f;
        anchors[1] = 90.f;
        anchors[2] = 156.f;
        anchors[3] = 198.f;
        anchors[4] = 373.f;
        anchors[5] = 326.f;

        std::vector<Object> objects32;
        generate_proposals(anchors, 32, in_pad, out, prob_threshold, objects32);

        proposals.insert(proposals.end(), objects32.begin(), objects32.end());
    }

    // sort all proposals by score from highest to lowest
    qsort_descent_inplace(proposals);

    // apply nms with nms_threshold
    std::vector<int> picked;
    nms_sorted_bboxes(proposals, picked, nms_threshold);

    int count = picked.size();

    objects.resize(count);
    for (int i = 0; i < count; i++)
    {
        objects[i] = proposals[picked[i]];

        // adjust offset to original unpadded
        float x0 = (objects[i].rect.x - (wpad / 2)) / scale;
        float y0 = (objects[i].rect.y - (hpad / 2)) / scale;
        float x1 = (objects[i].rect.x + objects[i].rect.width - (wpad / 2)) / scale;
        float y1 = (objects[i].rect.y + objects[i].rect.height - (hpad / 2)) / scale;

        // clip
        x0 = std::max(std::min(x0, (float)(img_w - 1)), 0.f);
        y0 = std::max(std::min(y0, (float)(img_h - 1)), 0.f);
        x1 = std::max(std::min(x1, (float)(img_w - 1)), 0.f);
        y1 = std::max(std::min(y1, (float)(img_h - 1)), 0.f);

        objects[i].rect.x = x0;
        objects[i].rect.y = y0;
        objects[i].rect.width = x1 - x0;
        objects[i].rect.height = y1 - y0;
    }

    return 0;
}

inline int
conn_nonb(struct sockaddr_in sa, int sock, int timeout)
{
    int flags = 0, error = 0, ret = 0;
    fd_set  rset, wset;
    socklen_t   len = sizeof(error);
    struct timeval  ts;

    ts.tv_sec = 0;
    ts.tv_usec = timeout;

    //clear out descriptor sets for select
    //add socket to the descriptor sets
    FD_ZERO(&rset);
    FD_SET(sock, &rset);
    wset = rset;    //structure assignment ok

    //set socket nonblocking flag
    if( (flags = fcntl(sock, F_GETFL, 0)) < 0)
        return -1;

    if(fcntl(sock, F_SETFL, flags | O_NONBLOCK) < 0)
        return -1;

    //initiate non-blocking connect
    if( (ret = connect(sock, (struct sockaddr *)&sa, 16)) < 0 )
        if (errno != EINPROGRESS)
            return -1;

    if(ret == 0)    //then connect succeeded right away
        goto done;

    //we are waiting for connect to complete now
    if( (ret = select(sock + 1, &rset, &wset, NULL, (timeout) ? &ts : NULL)) < 0)
        return -1;
    if(ret == 0){   //we had a timeout
        errno = ETIMEDOUT;
        return -1;
    }

    //we had a positivite return so a descriptor is ready
    if (FD_ISSET(sock, &rset) || FD_ISSET(sock, &wset)){
        if(getsockopt(sock, SOL_SOCKET, SO_ERROR, &error, &len) < 0)
            return -1;
    }else
        return -1;

    if(error){  //check if we had a socket error
        errno = error;
        return -1;
    }

done:
    //put socket back in blocking mode
    if(fcntl(sock, F_SETFL, flags) < 0)
        return -1;

    return 0;
}

static void draw_objects(cv::Mat& bgr, const std::vector<Object>& objects)
{
    std::vector<Object> use_objects;
    std::cout << "\nNo. of Objects: " << objects.size();

    for(Object object : objects)
    {
        std::cout << object.label;
        if ((object.label < 20) && (object.label >= 0))
        {
            use_objects.push_back(object);
        }
    }

    int IDs[use_objects.size()];
    float distances[use_objects.size()];
    float angles[use_objects.size()];
    float widths[use_objects.size()];

    for (size_t i = 0; i < use_objects.size(); i++)
    {
        const Object& obj = use_objects[i];

        #if SEND_PACKET
            if(obj.label < 20)
            {
                float distance = object_distance(obj.label, int(obj.rect.height));
                float angle = object_angle(int(obj.rect.x) + int(obj.rect.width / 2));
                float width = object_width(obj.label, int(obj.rect.height), int(obj.rect.width));
                IDs[i] = obj.label;
                printf("%d", obj.label);
                distances[i] = distance;
                angles[i] = angle;
                widths[i] = width;
            }
        #endif // SEND_PACKET


        fprintf(stderr, "%d = %.5f at %.2f %.2f %.2f x %.2f\n", obj.label, obj.prob,
                obj.rect.x, obj.rect.y, obj.rect.width, obj.rect.height);

        #if DRAW_BOXES
            cv::rectangle(bgr, obj.rect, cv::Scalar(255, 0, 0));

            char text[256];
            sprintf(text, "%s %.1f%%", class_names[obj.label], obj.prob * 100);

            int baseLine = 0;
            cv::Size label_size = cv::getTextSize(text, cv::FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);

            int x = obj.rect.x;
            int y = obj.rect.y - label_size.height - baseLine;
            if (y < 0)
                y = 0;
            if (x + label_size.width > bgr.cols)
                x = bgr.cols - label_size.width;

            cv::rectangle(bgr, cv::Rect(cv::Point(x, y), cv::Size(label_size.width, label_size.height + baseLine)),
                          cv::Scalar(255, 255, 255), -1);

            cv::putText(bgr, text, cv::Point(x, y + label_size.height),
                        cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 0));
        #endif // DRAW_BOXES
    }

    for (int i = 0; i < objects.size(); i++)
    {
        printf("-%d-", IDs[i]);
    }



    #if SEND_PACKET
        int s;
        s = socket(PF_INET, SOCK_STREAM, 0);
        if (s < 0)
        {
            printf("Socket Failed!");
            perror("socket");
        }


        struct sockaddr_in s_in;


        s_in.sin_family = PF_INET;
        s_in.sin_port = htons(9999);
        s_in.sin_addr.s_addr=inet_addr("169.254.56.154");
        int con = conn_nonb(s_in,s,10000);
        if(con==-1)
        {
            printf("Connection Failed!");
            perror("Con");
        }

        std::cout << "Socket is Ready";

        printf("\nStarting Serialisation\n");
        char IDsString[512] = "";
        char distancesString[512] = "";
        char anglesString[512] = "";
        char widthsString[512] = "";
        for (int i = 0; i < objects.size(); ++i)
        {
            sprintf(IDsString, "%s,%d", IDsString, IDs[i]);
            sprintf(distancesString, "%s,%f", distancesString, distances[i]);
            sprintf(anglesString, "%s,%f", anglesString, angles[i]);
            sprintf(widthsString, "%s,%f", widthsString, widths[i]);
        }
        char message[2048];
        sprintf(message, "%d,%f%s%s%s%s", 0, 0.0f, IDsString, distancesString, anglesString, widthsString);
        // message = "0, 0.0, 0, 10.0, 1.0, 4.0";
        printf("\nFinished Serialising\n");
        printf(message);
        printf("\nStart Loop");
        //char message[2048];
        printf("\nAbout to serialize packet");
        printf("\nAbout to send Message");
        send(s , message, strlen(message) , 0 );
        printf("\nMessage Sent: %s\n", message);
        close(s);

    #endif // SEND_PACKET

}

#if USE_CAMERA
std::string gstreamer_pipeline(int capture_width, int capture_height, int framerate, int display_width, int display_height) {
    return
            " libcamerasrc ! video/x-raw, "
            " width=" + std::to_string(capture_width) + ","
            " height=" + std::to_string(capture_height) + ","
            " framerate=" + std::to_string(framerate) +"/1 !"
            "videoconvert !  video/x-raw, format=BGR ! appsink, drop=true";
}
#endif // USE_CAMERA

int main(int argc, char** argv)
{
    yolov5.register_custom_layer("YoloV5Focus", YoloV5Focus_layer_creator);

    // original pretrained model from https://github.com/ultralytics/yolov5
    // the ncnn model https://github.com/nihui/ncnn-assets/tree/master/models
    yolov5.load_param("yolov5s.param");
    yolov5.load_model("yolov5s.bin");


    //auto start = std::chrono::system_clock::now();

    #if USE_CAMERA
        std::string pipeline = gstreamer_pipeline(640, 360, 30, 640, 480);

        std::cout << "\nUsing pipeline: \n\t" << pipeline << "\n\n\n";

        auto start = std::chrono::system_clock::now();
        std::cout << "Opening Pipeline...\n";
        cv::VideoCapture videoCapture(pipeline, cv::CAP_GSTREAMER);
        auto end = std::chrono::system_clock::now();

        std::chrono::duration<double> elapsed_seconds = end-start;
        std::time_t end_time = std::chrono::system_clock::to_time_t(end);
        std::cout << "finished frame @ " << std::ctime(&end_time)
                  << "elapsed time: " << elapsed_seconds.count() << "s\n";

        if(!videoCapture.isOpened()) {
            std::cout<<"Failed to open camera."<<std::endl;
            return (-1);
        }

        std::cout << "\nPipeline Opened...\n";
    #else
        cv::VideoCapture videoCapture("Quincentennial_Bridge_R338.mp4");
    #endif // USE_CAMERA

    std::cout << "\nCreating inputFrame...\n";

    cv::Mat inputFrame;

    std::cout << "\ninputFrame Created...\n";

    std::cout << "\nStarting Inference...\n";

    //auto end = std::chrono::system_clock::now();

//        std::chrono::duration<double> elapsed_seconds = end-start;
//        std::time_t end_time = std::chrono::system_clock::to_time_t(end);
//        std::cout << "finished frame @ " << std::ctime(&end_time)
//                  << "elapsed time: " << elapsed_seconds.count() << "s\n";



    while(true)
    {

        auto start = std::chrono::system_clock::now();

        videoCapture.read(inputFrame);

        std::vector<Object> objects;
        detect_yolov5(inputFrame, objects);
        //usleep(200000);

        #if MARGINAL_GAINS
            draw_objects(inputFrame, objects);


            cv::imshow("YOLOv5", inputFrame);
            cv::imwrite("test.jpg",inputFrame);


        #endif // MARGINAL_GAINS

        //usleep(1750000);

        auto end = std::chrono::system_clock::now();

        std::chrono::duration<double> elapsed_seconds = end-start;
        std::time_t end_time = std::chrono::system_clock::to_time_t(end);
        std::cout << "finished frame @ " << std::ctime(&end_time)
                  << "elapsed time: " << elapsed_seconds.count() << "s\n";

        if (cv::waitKey(20) == 27) break;

    }
    return 0;
}
