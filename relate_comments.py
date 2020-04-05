import sys
import re
import nltk
import nltk.data
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from data.database.module import Post_Java,Comments,Posts_Java_And_Comments
from data.database.engine_factor import EngineFactory

#reload(sys)
sys.setdefaultencoding("utf-8")

def filter_posts_with_java_tag():
    # engine = create_engine("mysql+mysqldb://root:root@10.131.252.160/stackoverflow?charset=utf8", encoding='utf-8')
    # Session = sessionmaker(bind=engine)
    # session = Session()
    session = EngineFactory.create_session()
    posts = session.query(Posts_Android_Java).filter(Posts_Android_Java.Id >=700000,Posts_Android_Java.Id < 1000000,Posts_Android_Java.Tags.like("%<java>%")).all()
    for post in posts:
        print(post.Tags)
        xy_post = XY_posts_java(post.Id, post.PostTypeId,post.AcceptedAnswerId, post.ParentId, post.Score, post.ViewCount, post.Body, post.OwnerUserId,
                  post.OwnerDisplayName, post.LastEditorUserId, post.LastEditDate, post.LastActivityDate, post.Title, post.Tags, post.AnswerCount,
                  post.CommentCount, post.FavoriteCount, post.CreationDate)
        session.add(xy_post)
        session.commit()
    session.close()
def filter_answer_posts_with_java_tag():
    session = EngineFactory.create_session()
    posts = session.query(Posts_android_java_answer_index).join(XY_posts_java,XY_posts_java.ParentId==Posts_android_java_answer_index.Id).all()
    for post in posts:
        xy_post = XY_posts_java(post.Id, post.PostTypeId, post.AcceptedAnswerId, post.ParentId, post.Score,
                                post.ViewCount, post.Body, post.OwnerUserId,
                                post.OwnerDisplayName, post.LastEditorUserId, post.LastEditDate, post.LastActivityDate,
                                post.Title, post.Tags, post.AnswerCount,
                                post.CommentCount, post.FavoriteCount, post.CreationDate)
        session.add(xy_post)
        session.commit()
    session.close()
def post_relate_to_comments():
    session = EngineFactory.create_session()
    posts = session.query(Post_Java).all()
    postId = 1
    for post in posts:
        text = ""

        java_posts = session.query(Comments).join(Post_Java,Comments.PostId == post.Id).all()
        for java_post in java_posts:
            text=text+'\n'+java_post.Text
        new_post = Posts_Java_And_Comments(post.Id,post.PostTypeId,post.AcceptedAnswerId,
                                           post.ParentId,post.Score,post.Body,post.OwnerUserId,post.Title,post.Tags,
                                           post.AnswerCount,post.CommentCount,text)
        session.add(new_post)
        session.commit()
    session.close()

 




filter_posts_with_java_tag()


