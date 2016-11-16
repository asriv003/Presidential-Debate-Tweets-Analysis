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
        
        /*ArrayWritable arrayWritable = new ArrayWritable(Text.class);

        Text [] textValues = new Text[2];
        textValues[0] = new Text("value1");
        textValues[1] = new Text("value1");

        arrayWritable.set(textValues );
        context.write(key , arrayWritable );*/
        //List of cities per conference
        private final static Text conf = new Text();
        private Text word = new Text();

        public void map(Object key, Text value, Context context) 
                throws IOException, InterruptedException {
            //Input whole String
            String str = value.toString();
            //Splitting by tab
            String[] values = str.split("\t");
            //Setting key as Conference City
            word.set(values[3]);
            //Setting Value as Conference
            conf.set(values[0]);
            context.write(word, conf);
        }
    }

  public static class ListSumReducer
        extends Reducer<Text,Text,Text,ArrayWritable> {
      private ArrayWritable result = new ArrayWritable(Text.class);
      public void reduce(Text key, Iterable<Text> values,Context context)
            throws IOException, InterruptedException {
          Text[] textValues = new Text();
          int index = 0;
          for (Text val : values) {
              textValues[index] = new Text(val);
              index++;
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
      job.setOutputValueClass(ArrayWritable.class);
      FileInputFormat.addInputPath(job, new Path(args[0]));
      FileOutputFormat.setOutputPath(job, new Path(args[1]));
      System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}