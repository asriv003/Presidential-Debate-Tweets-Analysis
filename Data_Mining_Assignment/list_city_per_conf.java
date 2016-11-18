import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {

    public static class TokenizerMapper
            extends Mapper<Object, Text, Text, Text>{
        //List of cities per conference
        private final static Text conf = new Text();
        private Text word = new Text();

        public void map(Object key, Text value, Context context) 
                throws IOException, InterruptedException {
            //Input whole String
            String str = value.toString();
            //Splitting by tab
            String[] values = str.split(",");
            //Setting key as Conference City
            word.set(values[3]);
            //Setting Value as Conference Name
            conf.set(values[0]);
            context.write(word, conf);
        }
    }

  public static class ListSumReducer
        extends Reducer<Text,Text,Text,Text> {
      private Text result = new Text();
      public void reduce(Text key, Iterable<Text> values,Context context)
            throws IOException, InterruptedException {
          //final string of all the conference names for a particular city
          String textValues = "";
          for (Text val : values) {
              //To avoid repetation of same conference in the same city
              if(!textValues.contains(val.toString())) {
                //Appending string to textValues
                textValues = textValues + val.toString() + " ";
              }
          }
          result.set(textValues);
          context.write(key, result);
      }
  }

  public static void main(String[] args) throws Exception {
      Configuration conf = new Configuration();
      Job job = Job.getInstance(conf, "word count");
      job.setJarByClass(WordCount.class);
      job.setMapperClass(TokenizerMapper.class);
      job.setCombinerClass(ListSumReducer.class);
      job.setReducerClass(ListSumReducer.class);
      job.setOutputKeyClass(Text.class);
      job.setOutputValueClass(Text.class);
      FileInputFormat.addInputPath(job, new Path(args[0]));
      FileOutputFormat.setOutputPath(job, new Path(args[1]));
      System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}