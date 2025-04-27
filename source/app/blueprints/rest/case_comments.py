#  IRIS Source Code
#  DFIR-IRIS Team
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import marshmallow

from flask import request

from app.schema.marshables import CommentSchema
from app.blueprints.responses import response_error
from app.blueprints.responses import response_success
from app.business.case_comments import case_comments_update
from app.business.errors import BusinessProcessingError


def case_comment_update(comment_id, object_type, caseid):
    try:
        comment_schema = CommentSchema()
        rq_t = request.get_json()
        comment_text = rq_t.get('comment_text')
        comment = case_comments_update(comment_text, comment_id, object_type, caseid)
        return response_success("Comment edited", data=comment_schema.dump(comment))
    except BusinessProcessingError as e:
        return response_error(e.get_message(), data=e.get_data())
    except marshmallow.exceptions.ValidationError as e:
        return response_error(msg='Data error', data=e.normalized_messages())
